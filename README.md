# Risk-Informed Response (RIR) Dashboard

## QUICK INSTALLATION GUIDE

# Production
```
git clone https://github.com/kartoza/rir-dashboard.git
cd rir-dashboard/deployment
docker-compose up -d
```

The web will be available at `http://127.0.0.1/`

To stop containers:
```
docker-compose kill
```

To stop and delete containers:
```
docker-compose down
```


# Development
```
git clone https://github.com/kartoza/rir-dashboard.git
cd rir-dashboard/deplyment
cp .template.env .env
docker-compose.override.template.yml docker-compose.override.yml

cd rir-dashboard
make up
make dev
```

The web will be available at `http://localhost:2000/`

To stop dev:
```
make dev-kill
```

To reload container:
```
make dev-reload
```

# Setup onedrive:
1. Download onedrive by `sudo apt-get install onedrive`
2. Execute `onedrive --get-O365-drive-id '<your site name to search>'`
3. It will ask to click an url and put back the url that created on browser
4. It will show an information. Check drive_id and copy it.
5. Go to deployment/onedrive/config
6. Put it to drive_id
7. Execute `make onedrive-volume`
8. Execute `docker volume inspect onedrive-volume`
9. It will show a volume, copy the path of volume.
10 Copy the deployment/onedrive/config to the above volume.
11. `make onedrive-firstrun` to run first config
12. It will ask to click an url and put back the url that created on browser
13. Wait the system to finish the sync
14. After that we can stop it and do `make up`

More information:
https://github.com/abraunegg/onedrive/blob/master/docs/SharePoint-Shared-Libraries.md