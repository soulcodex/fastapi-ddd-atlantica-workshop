SHELL := /bin/bash
DOCKER_COMPOSE := docker compose -f docker-compose.yml

.PHONY: help
help:
	@cat $(MAKEFILE_LIST) | grep -e "^[a-zA-Z_\-]*: *.*## *" | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: setup
setup: ## Make shoes api setup
	[ -f ./docker-compose.yml ] || cp docker-compose.yml.dist docker-compose.yml
	[ -f ./.env ] || cp .env.example .env
	$(DOCKER_COMPOSE) up -d --build --force-recreate

.PHONY: stop
stop: ## Stop project docker containers.
	$(DOCKER_COMPOSE) down --remove-orphans

.PHONY: start
start: ## Bootstrap and run shoes api
	pipenv install
	pipenv run pyway migrate
	pipenv run uvicorn main:app --reload --loop asyncio --reload-include $$PWD/../../apps --reload-include $$PWD/../../shoes --reload-include $$PWD/../../shared

.PHONY: install-dep
install-dep: ## Install a new dependency using pipenv environment
	DEP=$(shell bash -c 'read -p "Package name to install: " dep; echo $$dep') && \
	pipenv install $$DEP


.PHONY: remove-dep
remove-dep: ## Remove a specific dependency using pipenv environment deps file.
	PS3="Select the package to uninstall: " && \
	select pkg in $$(yq '.packages * .dev-packages|keys|join(" ")' -oy -p toml Pipfile); \
	do \
	  if [ ! -z $$pkg ]; then \
	  	pipenv uninstall $$pkg; \
	  	exit; \
	  fi; \
	  echo "Invalid package selected" && exit; \
  	done