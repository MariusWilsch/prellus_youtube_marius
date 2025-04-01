.PHONY: up down logs monitor watch

up:
	docker compose up -d
	@echo "Starting services..."
	@sleep 3
	@echo "Opening portal..."
	open http://localhost:3000

down:
	docker compose down

logs:
	docker compose logs -f

monitor:
	docker compose ps
	@echo "\nResource Usage:"
	docker stats --no-stream $(docker compose ps -q)