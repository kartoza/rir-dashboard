SHELL := /bin/bash

run:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Run the docs container"
	@echo "Can be accessed in http://localhost:8000/"
	@echo "------------------------------------------------------------------"
	docker run --rm -d -p 8000:8000 --name mkdocs -v ${shell pwd}:/docs squidfunk/mkdocs-material

down:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Down mkdocs"
	@echo "------------------------------------------------------------------"
	docker rm -f mkdocs

