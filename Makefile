SHELL := /usr/bin/env bash
COMPOSE := docker compose -p tda-geo -f docker-compose.yml

.PHONY: up up-dev up-jupyter down rebuild logs-dev logs-jupyter ps seed-reset prune

up: up-dev up-jupyter

up-dev:
	$(COMPOSE) up -d dev

up-jupyter:
	$(COMPOSE) up -d jupyter

down:
	$(COMPOSE) down --remove-orphans

rebuild:
	$(COMPOSE) down --remove-orphans
	$(COMPOSE) build --pull --no-cache
	$(COMPOSE) up -d dev

logs-dev:
	docker logs -f --tail=200 tda-geo-dev

logs-jupyter:
	docker logs -f --tail=200 tda-geo-jupyter

ps:
	$(COMPOSE) ps

seed-reset:
	# blow away the conda volume to force reseed next start
	-docker volume rm $$(docker volume ls -q | grep tda-geo_conda_store)
	$(COMPOSE) up -d dev

prune:
	docker system prune -f
