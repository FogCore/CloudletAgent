import os
import docker

docker_client = docker.from_env()
cloudlet_info = {}
cloudlets_service_url = os.environ.get('CLOUDLETS_SERVICE_URL')
cloudlet_info_file_path = 'cloudlet_info.txt'
