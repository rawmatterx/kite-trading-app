.PHONY: help install start stop restart logs clean test migrate lint format check

# Colors
RED=\033[0;31m
GREEN=\033[0;32m
YELLOW=\033[0;33m
NC=\033[0m # No Color

# Variables
SERVICE=

help:
	@echo "\n${YELLOW}Available commands:${NC}"
	@echo "${GREEN}make install${NC}    - Install all dependencies"
	@echo "${GREEN}make start${NC}     - Start all services"
	@echo "${GREEN}make stop${NC}      - Stop all services"
	@echo "${GREEN}make restart${NC}   - Restart all services"
	@echo "${GREEN}make logs${NC}      - View logs (use SERVICE=backend or SERVICE=frontend for specific service)"
	@echo "${GREEN}make clean${NC}     - Remove all containers, networks, and volumes"
	@echo "${GREEN}make test${NC}      - Run tests"
	@echo "${GREEN}make migrate${NC}   - Run database migrations"
	@echo "${GREEN}make lint${NC}      - Run linter"
	@echo "${GREEN}make format${NC}    - Format code"
	@echo "${GREEN}make check${NC}     - Check code style and types"

install:
	@echo "\n${GREEN}Installing dependencies...${NC}"
	docker-compose -f docker-compose.yml -f docker-compose.override.yml build

start:
	@echo "\n${GREEN}Starting services...${NC}"
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

stop:
	@echo "\n${YELLOW}Stopping services...${NC}"
	docker-compose -f docker-compose.yml -f docker-compose.override.yml down

restart: stop start

logs:
	@if [ -z "$(SERVICE)" ]; then \
		echo "\n${YELLOW}Viewing logs for all services${NC}"; \
		docker-compose -f docker-compose.yml -f docker-compose.override.yml logs -f; \
	else \
		echo "\n${YELLOW}Viewing logs for $(SERVICE)${NC}"; \
		docker-compose -f docker-compose.yml -f docker-compose.override.yml logs -f $(SERVICE); \
	fi

clean:
	@echo "\n${RED}Cleaning up...${NC}"
	docker-compose -f docker-compose.yml -f docker-compose.override.yml down -v --remove-orphans

test:
	@echo "\n${GREEN}Running tests...${NC}"
	docker-compose -f docker-compose.yml -f docker-compose.override.yml run --rm backend pytest -v

migrate:
	@echo "\n${GREEN}Running migrations...${NC}"
	docker-compose -f docker-compose.yml -f docker-compose.override.yml run --rm backend alembic upgrade head

lint:
	@echo "\n${YELLOW}Running linter...${NC}"
	docker-compose -f docker-compose.yml -f docker-compose.override.yml run --rm backend flake8 .

format:
	@echo "\n${GREEN}Formatting code...${NC}"
	docker-compose -f docker-compose.yml -f docker-compose.override.yml run --rm backend black .
	docker-compose -f docker-compose.yml -f docker-compose.override.yml run --rm backend isort .

check:
	@echo "\n${YELLOW}Checking code style and types...${NC}"
	docker-compose -f docker-compose.yml -f docker-compose.override.yml run --rm backend black --check .
	docker-compose -f docker-compose.yml -f docker-compose.override.yml run --rm backend isort --check-only .
	docker-compose -f docker-compose.yml -f docker-compose.override.yml run --rm backend mypy .

# Add more targets as needed
