import json
import grpc
import docker
import requests
import subprocess
from google.protobuf.json_format import MessageToJson
from CloudletAgent import (
    cloudlet_agent_pb2, cloudlet_agent_pb2_grpc,
    docker_client, cloudlets_service_url, cloudlet_info_file_path
)


# Reads the field and cast it to the required type
def required_type_input(message, old_value):
    while True:
        print(message, f'[{old_value}]: ', end='')
        new_value = ''
        while True:
            new_value = input()
            if old_value:
                break
            if not new_value:
                print('Empty value is not valid.')
                print(message, f'[{old_value}]: ', end='')
            else:
                break

        if not new_value:
            new_value = old_value

        try:
            return type(old_value)(new_value)
        except ValueError:
            print('Unexpected value.')


# Registers a new fog device in the system
def register_cloudlet():
    print('It looks like the first cloudlet start. Register cloudlet:\n')

    while True:
        name = required_type_input('Enter the cloudlet name', str(subprocess.run('hostname', shell=True, text=True, stdout=subprocess.PIPE).stdout)[:-1])
        cpu_cores = required_type_input('Enter the number of CPU cores', int(subprocess.run('nproc', shell=True, text=True, stdout=subprocess.PIPE).stdout))
        cpu_frequency = required_type_input('Enter the CPU frequency',
                                            float(subprocess.run('lscpu | grep "MHz"',
                                                                 shell=True,
                                                                 text=True,
                                                                 stdout=subprocess.PIPE).stdout.split()[-1]))
        ram_size = required_type_input('Enter the RAM amount',
                                       int(subprocess.run('echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE)))',
                                                          shell=True, text=True,
                                                          stdout=subprocess.PIPE).stdout))
        rom_size = required_type_input('Enter the ROM amount',
                                       int(subprocess.run('df --block-size=1 / | grep /',
                                                          shell=True, text=True,
                                                          stdout=subprocess.PIPE).stdout.split()[1]))
        os = required_type_input('Enter the OS name',
                                 str(subprocess.run('lsb_release -d',
                                                    shell=True,
                                                    text=True,
                                                    stdout=subprocess.PIPE).stdout.split('\t')[1][:-1]))
        os_kernel = required_type_input('Enter the kernel version', str(subprocess.run('uname -r', shell=True, text=True, stdout=subprocess.PIPE).stdout[:-1]))
        ipinfo = requests.get(url='http://ipinfo.io').json()
        ip = required_type_input('Enter IP address', ipinfo['ip'])
        latitude = required_type_input('Enter the latitude', float(ipinfo['loc'].split(',')[0]))
        longitude = required_type_input('Enter the longitude', float(ipinfo['loc'].split(',')[1]))
        country = required_type_input('Enter the country', ipinfo['country'])
        region = required_type_input('Enter the region', ipinfo['region'])
        city = required_type_input('Enter the city', ipinfo['city'])

        print('\n\nPlease check your entries:',
              f'Cloudlet name:\t{name}',
              f'Number of CPU:\t{cpu_cores}',
              f'CPU frequency:\t{cpu_frequency}',
              f'RAM amount:\t{ram_size}',
              f'ROM amount:\t{rom_size}',
              f'OS name:\t{os}',
              f'Kernel version:\t{os_kernel}',
              f'IP address:\t{ip}',
              f'Latitude:\t{latitude}',
              f'Longitude:\t{longitude}',
              f'Country:\t{country}',
              f'Region:\t\t{region}',
              f'City:\t\t{city}',
              sep='\n')

        while True:
            answer = input('\nAre the data entered correctly? [Y/n]: ')
            if answer in ['', 'Y', 'y', 'N', 'n']:
                break

        if answer in ['', 'Y', 'y']:
            break

        print()

    # Call the remote method to register the fog device in Cloudlets Service
    with grpc.insecure_channel(cloudlets_service_url) as channel:
        stub = cloudlet_agent_pb2_grpc.CloudletsAPIStub(channel)
        registration_response = stub.Add(cloudlet_agent_pb2.Cloudlet(name=name,
                                                                     cpu_cores=cpu_cores,
                                                                     cpu_frequency=cpu_frequency,
                                                                     ram_size=ram_size,
                                                                     rom_size=rom_size,
                                                                     os=os,
                                                                     os_kernel=os_kernel,
                                                                     ip=ip,
                                                                     latitude=latitude,
                                                                     longitude=longitude,
                                                                     country=country,
                                                                     region=region,
                                                                     city=city))

        print(f'\nRegistration status:\n\tCode: {registration_response.status.code}\n\tMessage: {registration_response.status.message}')

        if registration_response.status.code in [201, 409]:
            subprocess.run('hostnamectl set-hostname ' + registration_response.cloudlet.id, shell=True)
            print('\nJoin to Swarm status: ')
            success = False
            try:
                docker_client.swarm.join(remote_addrs=[registration_response.swarm_manager_address],
                                         join_token=registration_response.swarm_worker_token)
                success = True
            except docker.errors.APIError as error:
                print(f'\t{error}')
                if str(error) == '503 Server Error: Service Unavailable ("This node is already part of a swarm. Use "docker swarm leave" to leave this swarm and join another one.")':
                    success = True
            if success:
                print('\tSuccess\n')
                with open(cloudlet_info_file_path, 'w') as file:
                    data = MessageToJson(registration_response.cloudlet)
                    file.write(data)
                    return json.loads(data)
        exit(0)
