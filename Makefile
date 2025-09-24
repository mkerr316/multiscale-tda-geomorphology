.PHONY: up down rebuild shell prune gpu

up:
	docker compose up -d

down:
	docker compose down

rebuild:
	docker compose build

shell:
	docker exec -it tda-geo bash

gpu:
	docker exec -it tda-geo python -c "import torch;print('CUDA OK:',torch.cuda.is_available(),'Devices:',torch.cuda.device_count())"

prune:
	docker container prune -f && docker image prune -f && docker system prune -f
