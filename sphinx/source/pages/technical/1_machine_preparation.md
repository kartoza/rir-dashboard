# Setup the Machine

## Install make dependency

This will install make on your machine or virtual box server

```
sudo apt install make       # version 4.2.1-1.2       
```

## Install docker-compose

This will install docker-compose on your machine or virtual box server

```
sudo apt install docker-compose       
```

## Run apt update

This will run apt update
```
sudo apt-get update       
```
## Run apt install

This will run apt install
```
apt install \
ca-certificates \
curl \
gnup \
lsb-release
```

## Download docker

This will download docker 

```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg     
```

On the next prompt line:

```
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg]https:download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Run apt update:

```
sudo apt-get update
```

## Install docker

This will install docker
```
sudo apt-get install  docker-ce-cli containerd.io
```

## Check if installation was successful

This will check if installation of docker was successful
```
sudo docker version
```
And it should return like this

```
Client: Docker Engine - Community
 Version:           20.10.9
 API version:       1.41
 Go version:        go1.16.8
 Git commit:        c2ea9bc
 Built:             Mon Oct  4 16:08:29 2021
 OS/Arch:           linux/amd64
 Context:           default
 Experimental:      true

```

## Manage docker as non-root

This will ensure that the docker can be executed without sudo.
```
sudo systemctl daemon-reload
sudo systemctl start docker
sudo usermod -a -G $USER
sudo systemctl enable docker
```

Verify that you can run docker commands without sudo.
```
docker run hello-world
```

For more information how to install docker, please visit [Install Docker Engine](https://docs.docker.com/engine/install/)