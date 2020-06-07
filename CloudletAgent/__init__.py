import os
import docker
import pathlib

docker_client = docker.from_env()
cloudlet_info = {}
cloudlets_service_url = os.environ.get('CLOUDLETS_SERVICE_URL')
cloudlet_info_file_path = str(pathlib.Path().absolute()) + '/cloudlet_info.txt'
