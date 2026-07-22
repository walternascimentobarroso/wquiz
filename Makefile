# File variables
FILE1 = .env
FILE2 = .env.example

# Check if .env file exists
ifeq (,$(wildcard $(FILE1)))
$(shell cp $(FILE2) $(FILE1))
endif

# Load environment variables
include .env
export $(shell sed 's/=.*//' .env)

# Color Config
NOCOLOR=\033[0m
GREEN=\033[0;32m
BGREEN=\033[1;32m
YELLOW=\033[0;33m
CYAN=\033[0;36m
RED=\033[0;31m

# Config
BREAK=\n

# Default action
.DEFAULT_GOAL := help

# Checks if the docker-compose command is available in the system
DOCKER_COMPOSE := $(shell command -v docker-compose 2> /dev/null)

# If Docker-Compose is available, use it, otherwise it uses docker compose
ifeq ($(strip $(DOCKER_COMPOSE)),)
	DOCKER_COMPOSE := docker compose
else
	DOCKER_COMPOSE := docker-compose
endif

## General commands:
.PHONY: help
help: ## Display this message help
	@awk '\
		BEGIN {\
			FS = ":.*##";\
			printf "${BREAK}${YELLOW}Usage:${BREAK}${CYAN}  make [target]${BREAK}${BREAK}${YELLOW}Available targets:${BREAK}${BREAK}" \
		} /^##/ { \
			printf "${YELLOW}%s${NOCOLOR}${BREAK}", substr($$0, 4) \
		} /^[a-zA-Z0-9_-]+:.*?##/ { \
			printf "  ${BGREEN}%-18s${NOCOLOR} %s${BREAK}", $$1, $$2 \
		}' $(MAKEFILE_LIST)
	@printf "${BREAK}${YELLOW}Example:${BREAK}${CYAN}  make up${BREAK}"

.PHONY: build
build: ## Build all container
	@echo ""
	@echo "${YELLOW}Build all container${NOCOLOR}"
	@echo ""
	$(DOCKER_COMPOSE) up --build -d

.PHONY: rebuild
rebuild: destroy build ## Destroy and Rebuild all container

.PHONY: up
up: ## Start all container in detached mode
	@echo ""
	@echo "${YELLOW}Start all container${NOCOLOR}"
	@echo ""
	$(DOCKER_COMPOSE) up -d;

.PHONY: stop
stop: ## Stop all container
	@echo ""
	@echo "${YELLOW}Stop all container${NOCOLOR}"
	@echo ""
	$(DOCKER_COMPOSE) stop

.PHONY: restart
restart: stop up ## Restart all container

.PHONY: destroy
destroy: ## Destroy all container
	@echo ""
	@echo "${RED}Warning: This will destroy all container and data${NOCOLOR}"
	@echo "${YELLOW}Destroy all container${NOCOLOR}"
	@echo ""
	$(DOCKER_COMPOSE) down --remove-orphans -v

.PHONY: logs
logs: ## See LOG in backend container
	@echo ""
	@echo "${YELLOW}Log in backend container${NOCOLOR}"
	@echo ""
	$(DOCKER_COMPOSE) logs -f backend

.PHONY: ps
ps: ## List running containers
	$(DOCKER_COMPOSE) ps

## Backend commands:
.PHONY: backend-bash
backend-bash: ## Open shell in backend container
	@echo ""
	@echo "${YELLOW}Open shell in backend container${NOCOLOR}"
	@echo ""
	$(DOCKER_COMPOSE) exec backend bash

.PHONY: backend-logs
backend-logs: ## See LOG in backend container
	$(DOCKER_COMPOSE) logs -f backend

.PHONY: backend-shell
backend-shell: ## Open Python shell in backend
	@echo ""
	@echo "${YELLOW}Python shell in backend${NOCOLOR}"
	@echo ""
	$(DOCKER_COMPOSE) exec backend python

## Frontend commands:
.PHONY: frontend-bash
frontend-bash: ## Open shell in frontend container
	@echo ""
	@echo "${YELLOW}Open shell in frontend container${NOCOLOR}"
	@echo ""
	$(DOCKER_COMPOSE) exec frontend sh

.PHONY: frontend-logs
frontend-logs: ## See LOG in frontend container
	$(DOCKER_COMPOSE) logs -f frontend

## Admin commands:
.PHONY: admin-bash
admin-bash: ## Open shell in admin container
	@echo ""
	@echo "${YELLOW}Open shell in admin container${NOCOLOR}"
	@echo ""
	$(DOCKER_COMPOSE) exec admin sh

.PHONY: admin-logs
admin-logs: ## See LOG in admin container
	$(DOCKER_COMPOSE) logs -f admin

# Ignore make target errors for commands like `make backend bash`
.PHONY: %
%:
	@:
