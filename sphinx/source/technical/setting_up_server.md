# Setting up the server

## Steps for setting up server

### Clone rir-dashboard repository to your machine

This will clone the rir-dashboard rpository to your machine or virtual box
```
git clone https://github.com/kartoza/rir-dashboard.git
```

### Set up server

This will set up the rir-dashboard server on your machine or virtual box
```
cd rir-dashboard
cd deployment
cp docker-compose.override.template.yml docker-compose.override.yml
cp .template.env .env
cd ..
make up
docker ps
docker logs -f rir_dashboard_django
```

### Open server if using a linux machine

This will open the dashboard on a webpage:

Open up a web browser and go to 127.0.0.1 and the dashboard will open:
![RIR Dashboard on 127.0.0.1](../../img/rir-dashboard-linux-machine.PNG)

### If using a virtual box

Open network settings of your virtual box

![Network settings vbox](../../img/Virtualbox-network-settings1.PNG)

Click on port forwarding and add 2 new rules as indicated in the image below:

![Network settings 2 vbox](../../img/Virtualbox-network-settings2.PNG)

Click OK and close. Download [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html).
Create a connection by following these [directions](https://the.earth.li/~sgtatham/putty/0.67/htmldoc/Chapter2.html#gs-insecure), enter “localhost” as the host name, “SSH” as the protocol, and “2222” as the port.

Once you have logged in on PuTTY enter this command below in the prompt: 
```
ssh yourlogin@127.0.0.1 -p 22
```
(Make sure that you replace your username with "yourlogin")

When asked for your password, press enter three times and the prompt will display this message:  Permission denied (publickey,password).
 

Open the RIR dashboard server using a web browser on your machine by going to 127.0.0.1:8080
![RIR Dashboard on 127.0.0.1:8080](../../img/rir-dashboard-vbox.PNG)