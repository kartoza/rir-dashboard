# Preparing the server

## Basic Requirements

### You should be running a linux ubuntu server on your machine or on a virtual box

Ensure that you have set your unique login username and unique password

Start the server and login

### Install make dependency

This will install make on your machine or virtual box server

```
sudo apt install make       # version 4.2.1-1.2       
```

### Install docker-compose

This will install docker-compose on your machine or virtual box server

```
sudo apt install docker-compose       
```

### Run apt update

This will run apt update
```
sudo apt-get update       
```
### Run apt install

This will run apt install
```
apt install \
ca-certificates \
curl \
gnup \
lsb-release
```

### Download docker

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

### Install docker

This will install docker
```
sudo apt-get install  docker-ce-cli containerd.io
```

### Check if installation was successful

This will check if installation of docker was successful
```
sudo docker run hello-world
```
### Ensure that docker daemon is running on local host 

This will ensure that the docker daemon is running
```
sudo systemctl daemon-reload
sudo systemctl start docker
sudo usermod -a -G $USER
sudo systemctl enable docker
```

Restart the server

The docker daemon should be running now

