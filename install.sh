#!/bin/bash

echo
echo pip3 Installation
sudo apt install python3-pip -y

echo
echo Python packages Installation
pip3 install grpcio protobuf docker

echo
echo Docker Installation
curl -sSL https://get.docker.com | sh

echo
echo Adding insecure Docker Registry
read -p "Enter Docker Registry IP address or URL and port: " DOCKER_REGISTRY_IP
{ echo "{ \"insecure-registries\":[\"$DOCKER_REGISTRY_IP\"] }"; } | sudo tee /etc/docker/daemon.json

echo
echo Docker Restart
sudo service docker restart
