# Makefile for TDA Geomorphology Development Environment
SHELL := /usr/bin/env bash
COMPOSE_BASE := docker compose -f docker-compose.yml
COMPOSE_GPU := docker compose -f docker-compose.yml -f docker-compose.gpu.yml
COMPOSE := $(COMPOSE_GPU)  # Default to GPU mode
CONTAINER_NAME := tda-geo-dev

.DEFAULT_GOAL := help

# Color output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

##@ General

.PHONY: help
help: ## Display this help message
	@echo ""
	@echo "$(BLUE)TDA Geomorphology Development Environment$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make $(GREEN)<target>$(NC)\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(BLUE)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@echo ""

##@ Development

.PHONY: up
up: ## Start the development container (GPU mode)
	@echo "$(GREEN)Starting development container (GPU mode)...$(NC)"
	$(COMPOSE) up -d dev
	@echo "$(GREEN)✓ Container started!$(NC)"
	@echo "  - Jupyter Lab: http://localhost:8888"
	@echo "  - Dask Dashboard: http://localhost:8787"
	@make status

.PHONY: up-cpu
up-cpu: ## Start the development container (CPU-only mode)
	@echo "$(GREEN)Starting development container (CPU-only mode)...$(NC)"
	$(COMPOSE_BASE) up -d dev
	@echo "$(GREEN)✓ Container started!$(NC)"
	@echo "  - Jupyter Lab: http://localhost:8888"
	@echo "  - Dask Dashboard: http://localhost:8787"
	@make status

.PHONY: down
down: ## Stop all containers
	@echo "$(YELLOW)Stopping containers...$(NC)"
	$(COMPOSE) down --remove-orphans
	@echo "$(GREEN)✓ Containers stopped$(NC)"

.PHONY: restart
restart: down up ## Restart all containers

.PHONY: status
status: ## Show container status
	@echo ""
	@echo "$(BLUE)Container Status:$(NC)"
	@$(COMPOSE) ps
	@echo ""

##@ Building

.PHONY: build
build: ## Build the Docker image (GPU mode)
	@echo "$(GREEN)Building Docker image (GPU mode)...$(NC)"
	$(COMPOSE) build --pull
	@echo "$(GREEN)✓ Build complete!$(NC)"

.PHONY: build-cpu
build-cpu: ## Build the Docker image (CPU-only mode)
	@echo "$(GREEN)Building Docker image (CPU-only mode)...$(NC)"
	$(COMPOSE_BASE) build --pull
	@echo "$(GREEN)✓ Build complete!$(NC)"

.PHONY: rebuild
rebuild: ## Rebuild image from scratch (no cache)
	@echo "$(YELLOW)Rebuilding image from scratch...$(NC)"
	$(COMPOSE) down --remove-orphans
	$(COMPOSE) build --pull --no-cache
	$(COMPOSE) up -d dev
	@echo "$(GREEN)✓ Rebuild complete!$(NC)"

##@ Shell Access

.PHONY: shell
shell: ## Open a bash shell in the container
	@echo "$(GREEN)Opening shell in container...$(NC)"
	docker exec -it $(CONTAINER_NAME) bash -c 'export PATH="/opt/conda/envs/app/bin:/opt/conda/bin:/opt/conda/condabin:$$PATH"; exec bash'

.PHONY: shell-root
shell-root: ## Open a root bash shell in the container
	@echo "$(GREEN)Opening root shell in container...$(NC)"
	docker exec -it -u root $(CONTAINER_NAME) bash -c 'export PATH="/opt/conda/envs/app/bin:/opt/conda/bin:/opt/conda/condabin:$$PATH"; exec bash'

.PHONY: python
python: ## Start Python REPL in container
	@echo "$(GREEN)Starting Python REPL...$(NC)"
	docker exec -it $(CONTAINER_NAME) python

.PHONY: ipython
ipython: ## Start IPython REPL in container
	@echo "$(GREEN)Starting IPython REPL...$(NC)"
	docker exec -it $(CONTAINER_NAME) ipython

##@ Jupyter

.PHONY: jupyter-url
jupyter-url: ## Show Jupyter Lab URL with token
	@echo "$(GREEN)Jupyter Lab URL:$(NC)"
	@docker exec $(CONTAINER_NAME) jupyter server list 2>/dev/null || echo "  http://localhost:8888 (no token)"

.PHONY: jupyter-logs
jupyter-logs: ## Show Jupyter server logs
	@echo "$(GREEN)Jupyter Server Logs:$(NC)"
	@docker logs -f --tail=100 $(CONTAINER_NAME)

##@ Logs & Debugging

.PHONY: logs
logs: ## Follow container logs
	@echo "$(GREEN)Following container logs (Ctrl+C to exit)...$(NC)"
	docker logs -f --tail=200 $(CONTAINER_NAME)

.PHONY: logs-tail
logs-tail: ## Show last 50 lines of logs
	docker logs --tail=50 $(CONTAINER_NAME)

.PHONY: inspect
inspect: ## Inspect container configuration
	docker inspect $(CONTAINER_NAME)

.PHONY: health
health: ## Check container health status
	@echo "$(BLUE)Container Health:$(NC)"
	@docker inspect --format='{{.State.Health.Status}}' $(CONTAINER_NAME) 2>/dev/null || echo "No health check configured"

##@ Maintenance

.PHONY: seed-reset
seed-reset: ## Reset conda volume (forces fresh environment)
	@echo "$(YELLOW)Resetting conda volume...$(NC)"
	$(COMPOSE) down
	-docker volume rm tda-geo_conda_store
	@echo "$(GREEN)✓ Volume removed. Run 'make up' to reseed.$(NC)"

.PHONY: clean-volumes
clean-volumes: ## Remove all project volumes (data preserved)
	@echo "$(RED)Warning: This will remove all Docker volumes for this project!$(NC)"
	@echo "Your source code and data/ directory will NOT be affected."
	@read -p "Continue? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(COMPOSE) down -v; \
		echo "$(GREEN)✓ Volumes removed$(NC)"; \
	else \
		echo "$(YELLOW)Cancelled$(NC)"; \
	fi

.PHONY: prune
prune: ## Prune Docker system (careful!)
	@echo "$(YELLOW)Running Docker system prune...$(NC)"
	docker system prune -f
	@echo "$(GREEN)✓ Cleanup complete$(NC)"

.PHONY: deep-clean
deep-clean: ## Complete cleanup (containers, volumes, images)
	@echo "$(RED)Warning: This will remove EVERYTHING for this project!$(NC)"
	@read -p "Continue? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(COMPOSE) down -v --rmi all; \
		echo "$(GREEN)✓ Deep clean complete$(NC)"; \
	else \
		echo "$(YELLOW)Cancelled$(NC)"; \
	fi

##@ Testing & Quality

.PHONY: test
test: ## Run tests in container
	@echo "$(GREEN)Running tests...$(NC)"
	docker exec $(CONTAINER_NAME) pytest tests/

.PHONY: lint
lint: ## Run linter (ruff)
	@echo "$(GREEN)Running linter...$(NC)"
	docker exec $(CONTAINER_NAME) ruff check src/

.PHONY: format
format: ## Format code (ruff)
	@echo "$(GREEN)Formatting code...$(NC)"
	docker exec $(CONTAINER_NAME) ruff format src/

.PHONY: type-check
type-check: ## Run type checker (mypy)
	@echo "$(GREEN)Running type checker...$(NC)"
	docker exec $(CONTAINER_NAME) mypy src/

##@ Utilities

.PHONY: env-info
env-info: ## Show environment information
	@echo "$(BLUE)Environment Information:$(NC)"
	@echo ""
	docker exec $(CONTAINER_NAME) python -c "import sys; print(f'Python: {sys.version}')"
	@echo ""
	docker exec $(CONTAINER_NAME) python -c "import numpy, pandas, geopandas; print(f'NumPy: {numpy.__version__}'); print(f'Pandas: {pandas.__version__}'); print(f'GeoPandas: {geopandas.__version__}')"
	@echo ""
	@echo "$(BLUE)Conda environment:$(NC)"
	docker exec $(CONTAINER_NAME) conda list | head -20

.PHONY: update-deps
update-deps: ## Update conda environment from environment.yml
	@echo "$(GREEN)Updating dependencies...$(NC)"
	docker exec $(CONTAINER_NAME) micromamba update -n app -f /workspace/environment.yml -y
	@echo "$(GREEN)✓ Dependencies updated$(NC)"

##@ GPU Management

.PHONY: test-gpu-host
test-gpu-host: ## Test GPU access on host (before building)
	@echo "$(BLUE)Testing GPU access on host system...$(NC)"
	@echo ""
	docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi || \
		(echo "$(RED)✗ GPU test failed. Please check:$(NC)" && \
		 echo "  1. NVIDIA drivers installed (version >= 525)" && \
		 echo "  2. NVIDIA Container Toolkit installed" && \
		 echo "  3. Docker Desktop GPU support enabled" && \
		 exit 1)
	@echo ""
	@echo "$(GREEN)✓ GPU access confirmed!$(NC)"

.PHONY: test-gpu-container
test-gpu-container: ## Test GPU access in container (after starting)
	@echo "$(BLUE)Testing GPU access in container...$(NC)"
	@echo ""
	docker exec $(CONTAINER_NAME) nvidia-smi
	@echo ""
	@echo "$(GREEN)Testing PyTorch GPU support...$(NC)"
	docker exec $(CONTAINER_NAME) python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}'); print(f'GPU count: {torch.cuda.device_count()}'); print(f'GPU name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"
