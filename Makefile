.PHONY: help

help:  ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development
dev: ## Start docker-compose in development mode
	@docker compose -f ./deploy/docker-compose.dev.yml up -d

dev-build: ## Build docker-compose in development mode
	@docker compose -f ./deploy/docker-compose.dev.yml build

dev-logs: ## Show logs from all docker containers
	@docker compose -f ./deploy/docker-compose.dev.yml logs -f

dev-down: ## Stop all docker containers
	@docker compose -f ./deploy/docker-compose.dev.yml down

dev-db-delete: ## Delete development database
	@docker volume rm deploy_dev-db

dev-clean: ## Clean all dev images
	@docker images | grep 'pile-dev-be' | grep 'dev' | awk '{print $$3}' | xargs -r docker image rm
	@echo "Cleaned all dev images"

##@ Test
test: ## Run tests
	@docker compose -f deploy/docker-compose.test.yml up --exit-code-from pytest
	@docker container rm -f pile-dev-test pile-dev-db-test
