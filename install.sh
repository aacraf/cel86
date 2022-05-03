#!/bin/sh

# Docker_installation
if [ ! -x /var/lib/docker ]; then
        echo "INSTALLING docker"
echo
echo    #install docker dependencies 
        apt install apt-transport-https ca-certificates curl software-properties-common -y
echo
echo   #add docker’s official GPG key
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
echo
echo
        #set up the stable repository.
	add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"	
echo
echo
	#update the packages
	apt update -y

echo
echo
	#checks install from the Docker repo instead of the default Ubuntu repo:
	apt-cache policy docker-ce 
echo
echo

	#installing dcoker through docker-ce
	apt install docker-ce -y 
echo
echo
	#installing docker-compose
	apt install docker-compose -y
echo
echo
       #adds your username to the docker group
	usermod -aG docker ${USER}
       
       echo "docker successfully installed"

echo
echo

else

echo
echo
        echo "DOCKER ALREADY INSTALLED"
echo
echo

fi


# Installing the docker-compose file

apt-get install -y git

git clone https://github.com/node-red/node-red-docker.git

chmod +x spcapp/nodered_image/docker-debian.sh
bash spcapp/nodered_image/docker-debian.sh

docker run -d -p 1880:1880 -v node_red_data:/data --name myNRtest testing:node-red-build

docker build -t spcapp/nodered_image

docker-compose up
