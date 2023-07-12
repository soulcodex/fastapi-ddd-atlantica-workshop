PIPENV_VERSION_COMMAND := pipenv --version
YQ_VERSION_COMMAND := yq --version

__init:
	if [ ! command -v ${PIPENV_VERSION_COMMAND} 2> /dev/null ]; then @echo "pipenv installed" else @echo "pipenv not found"; @exit 1; fi;
	if [ ! command -v ${YQ_VERSION_COMMAND} 2> /dev/null ]; then @echo "yq installed" else @echo "yq not found"; @exit 1; fi;
 	export SHELL=/bin/bash
 	export ROOT_FOLDER=${PWD}
 	export SHOES_API_ROOT=${ROOT_FOLDER}/apps/shoes

.PHONY: help
help:
	@cat $(MAKEFILE_LIST) | grep -e "^[a-zA-Z_\-]*: *.*## *" | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

## Shoes API commands to manage

.PHONY: shoes-api
shoes-api: ## Setup shoes api dependencies.
	@make __init
	cd $$SHOES_API_ROOT && make setup

.PHONY: shoes-api-run
shoes-api-run: ## Bootstrap and run shoes api dev server.
	@make __init
	cd $$SHOES_API_ROOT && make start

.PHONY: shoes-api-docker-stop
shoes-api-docker-stop: ## Down docker containers related with the shoes service.
	@make __init
	cd $$SHOES_API_ROOT && make stop

.PHONY: shoes-api-package-add
shoes-api-package-add: ## Add package to our shoes api deps.
	@make __init
	cd $$SHOES_API_ROOT && make install-dep

.PHONY: shoes-api-package-remove
shoes-api-package-remove: ## Remove package from our shoes api deps.
	@make __init
	cd $$SHOES_API_ROOT && make remove-dep

.PHONY: shoes-api-unit-test
shoes-api-unit-test: ## Run unitary tests suite for shoes application.
	@make __init
	cd $$SHOES_API_ROOT && make unit-test