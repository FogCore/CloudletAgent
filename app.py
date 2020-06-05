#!/usr/bin/env python3

import json
import os.path
from CloudletAgent.registration import register_cloudlet
from CloudletAgent import cloudlet_info_file_path, cloudlet_info, cloudlets_service_url


if not cloudlets_service_url:
    print('Please set the environment variable CLOUDLETS_SERVICE_URL')
    exit(1)

if os.path.exists(cloudlet_info_file_path):
    with open(cloudlet_info_file_path, 'r') as file:
        try:
            cloudlet_info = json.loads(file.read())
        except json.decoder.JSONDecodeError:
            cloudlet_info = register_cloudlet()
else:
    cloudlet_info = register_cloudlet()

print(f'The cloudlet is registered:\n\tCloudlet ID: {cloudlet_info["id"]}.')
