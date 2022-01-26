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
cd rir-dashboard/deployment
make build
make up
make collectstatic
```

The web will be available at `http://127.0.0.1/`

To stop containers:
```
make kill
```

To stop and delete containers:
```
make rm
```
