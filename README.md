# Cloudlet Agent

Fog Node Agent is a software installed on every fog node. It is used to manage the device from the cloud, integrates its resources to the platform, supporting the deployment of the computational services. Ubuntu 20.04 OS is required for the correct work of the Agent on the fog node.



### Installation

1. Connect to a remote host via ssh

   ```bash
   ssh <username>@<host_ip>
   ```

4. Clone this repository and go to the created folder

   ```bash
git clone https://github.com/FogCore/CloudletAgent.git && cd CloudletAgent
   ```
   
3. Start the installation of the required components

   During the installation, you need to enter the IP address or domain name and port of the Docker Registry (see Images Service) in the following format `ip_address`:`port`

   ```bash
   sudo ./install.sh
   ```


5. Add a user to the docker group

   ```bash
   sudo usermod -aG docker $USER && newgrp - docker
   ```



### Running

1. Set the environment variable that defines the URL of Cloudlets Service

   ```bash
   export CLOUDLETS_SERVICE_URL="<ip_address>:<port>"
   ```

2. Run an agent.

   ```bash
   ./app.py
   ```
   

