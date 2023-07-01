SHELL := /bin/bash

.PHONY: help
help:
	@cat $(MAKEFILE_LIST) | grep -e "^[a-zA-Z_\-]*: *.*## *" | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: setup
setup: ## Make shoes api setup
	[ -f ./.env ] || cp .env.example .env

.PHONY: start
start: ## Bootstrap and run shoes api
	pipenv install
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
	  [ ! -v $$pkg ] || echo "Invalid package selected"; exit; \
	  pipenv uninstall $$pkg; \
	  exit; \
  	done