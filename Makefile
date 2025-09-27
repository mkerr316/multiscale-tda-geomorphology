.PHONY: build up-dev up-jupyter down shell prune gpu

# Build the shared Docker image for all services
build:
	docker compose build

# --- PyCharm Workflow ---
# Start the idle 'dev' container for PyCharm to connect to
up-dev:
	docker compose up -d dev

# --- Standalone Workflow ---
# Start the 'jupyter' service which runs the server directly
up-jupyter:
	docker compose up -d jupyter

# --- Common Commands ---
# Stop and remove all containers defined in this compose file
down:
	docker compose down

# Get a bash shell inside the running 'dev' container
shell:
	docker exec -it tda-geo-dev bash

# Check if CUDA is available in the 'dev' container
gpu:
	docker exec -it tda-geo-dev python -c "import torch;print('CUDA OK:',torch.cuda.is_available(),'Devices:',torch.cuda.device_count())"

# Clean up unused Docker resources
prune:
	docker container prune -f && docker image prune -f && docker system prune -f