PROJECT_ID := rir_dashboard
export COMPOSE_FILE=deployment/docker-compose.yml:deployment/docker-compose.override.yml
export ONEDRIVE_DATA_DIR=$(shell pwd)/deployment/onedrive

SHELL := /bin/bash

# ----------------------------------------------------------------------------
#    P R O D U C T I O N     C O M M A N D S
# ----------------------------------------------------------------------------
default: web
run: build web collectstatic

deploy: run
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Bringing up fresh instance "
	@echo "You can access it on http://localhost"
	@echo "------------------------------------------------------------------"

web:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose up -d

dev:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running in dev mode"
	@echo "------------------------------------------------------------------"
	@docker-compose ${ARGS} up -d dev
	@docker-compose ${ARGS} up --no-recreate --no-deps -d
	@docker exec $(PROJECT_ID)_dev python manage.py runserver 0.0.0.0:8080

dev-kill:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Kill dev"
	@echo "------------------------------------------------------------------"
	@docker kill $(PROJECT_ID)_dev

dev-reload: dev-kill dev
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Reload DEV"
	@echo "------------------------------------------------------------------"

build:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Building in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose build

nginx:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running nginx in production mode"
	@echo "Normally you should use this only for testing"
	@echo "In a production environment you will typically use nginx running"
	@echo "on the host rather if you have a multi-site host."
	@echo "------------------------------------------------------------------"
	@docker-compose up -d nginx
	@echo "Site should now be available at http://localhost"

up: web

status:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Show status for all containers"
	@echo "------------------------------------------------------------------"
	@docker-compose ps

kill:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Killing in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose stop

down: kill
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Removing production instance!!! "
	@echo "------------------------------------------------------------------"
	@docker-compose down

shell:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Shelling in in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose exec django /bin/bash

db-bash:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Entering DB Bash in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose exec db sh

db-shell:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Entering PostgreSQL Shell in production mode"
	@echo "------------------------------------------------------------------"
	docker-compose exec db su - postgres -c "psql"

collectstatic:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Collecting static in production mode"
	@echo "------------------------------------------------------------------"
	#@docker-compose run django python manage.py collectstatic --noinput
	#We need to run collect static in the same context as the running
	# django container it seems so I use docker exec here
	# no -it flag so we can run over remote shell
	@docker exec $(PROJECT_ID)_django python manage.py collectstatic --noinput

reload:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Reload django project in production mode"
	@echo "------------------------------------------------------------------"
	# no -it flag so we can run over remote shell
	@docker exec $(PROJECT_ID)_django django --reload  /tmp/django.pid

migrate:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running migrate static in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose exec django python manage.py migrate

onedrive-firstrun:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "First run one drive"
	@echo "------------------------------------------------------------------"
	@docker volume create $(PROJECT_ID)_onedrive-conf
	@mkdir -p ${ONEDRIVE_DATA_DIR}
	@docker run -it --name onedrive -v $(PROJECT_ID)_onedrive-conf:/onedrive/conf -v "${ONEDRIVE_DATA_DIR}:/onedrive/data" -e "ONEDRIVE_UID=1000" -e "ONEDRIVE_GID=1000" driveone/onedrive:latest

# --------------- help --------------------------------

help:
	@echo "* **build** - builds all required containers."
	@echo "* **up** - runs all required containers."
	@echo "* **kill** - kills all running containers. Does not remove them."
	@echo "* **logs** - view the logs of all running containers. Note that you can also view individual logs in the deployment/logs directory."
	@echo "* **nginx** - builds and runs the nginx container."
	@echo "* **permissions** - Update the permissions of shared volumes. Note this will destroy any existing permissions you have in place."
	@echo "* **rm** - remove all containers."
	@echo "* **shell-frontend-mapstore** - open a bash shell in the frontend mapstore (where django runs) container."
