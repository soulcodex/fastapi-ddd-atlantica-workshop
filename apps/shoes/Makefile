SHELL := /bin/bash
DOCKER_COMPOSE := docker compose -f docker-compose.yml
DOCKER_SHOES_EXEC := docker exec -it shoes-api-atlantica-conf-2023

.PHONY: help
help:
	@cat $(MAKEFILE_LIST) | grep -e "^[a-zA-Z_\-]*: *.*## *" | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: start
start: ## Make shoes api setup and start all shoes-api docker containers.
	[ -f ./docker-compose.yml ] || cp docker-compose.yml.dist docker-compose.yml
	[ -f ./.env ] || cp .env.example .env
	$(DOCKER_COMPOSE) up -d --build --force-recreate

.PHONY: bash
bash: ## Run bash terminal inside shoes-api container.
	$(DOCKER_SHOES_EXEC) bash -l

.PHONY: stop
stop: ## Stop project docker containers.
	$(DOCKER_COMPOSE) down --remove-orphans

.PHONY: install-dep
install-dep: ## Install a new dependency using pipenv environment
	DEP=$(shell bash -c 'read -p "Package name to install: " dep; echo $$dep') && \
	DEV=$(shell bash -c 'read -p "Is a development stage package? [yes|no] " dev; [$$dev != "yes"] || echo "--dev"') && \
	$(DOCKER_SHOES_EXEC) pipenv install $$DEP $$DEV

.PHONY: remove-dep
remove-dep: ## Remove a specific dependency using pipenv environment deps file.
	$(DOCKER_SHOES_EXEC) /root/tools/remove-dep.sh

.PHONY: unit-test
unit-test: ## Run shoes unitary tests.
	$(DOCKER_SHOES_EXEC) pipenv run pytest --no-header -v shoes/application/

.PHONY: acceptance-test
acceptance-test: ## Run shoes acceptance / E2E tests.
	$(DOCKER_SHOES_EXEC) pipenv run pytest --no-header -v tests/shoes/