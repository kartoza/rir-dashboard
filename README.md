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
