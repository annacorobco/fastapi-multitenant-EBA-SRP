PROJECT_NAME=fastapi-multitenant

# -------- DEV COMMANDS --------
dev-up:
	docker-compose -f docker-compose.dev.yml up --build

dev-down:
	docker-compose -f docker-compose.dev.yml down

dev-logs:
	docker-compose -f docker-compose.dev.yml logs -f

dev-bash:
	docker exec -it fastapi_app_dev bash

# Run Aerich migrations manually in dev
dev-migrate:
	docker exec -it fastapi_app_dev aerich migrate

dev-upgrade:
	docker exec -it fastapi_app_dev aerich upgrade


# -------- PROD COMMANDS --------
prod-up:
	docker-compose -f docker-compose.prod.yml up --build -d

prod-down:
	docker-compose -f docker-compose.prod.yml down

prod-logs:
	docker-compose -f docker-compose.prod.yml logs -f

prod-bash:
	docker exec -it fastapi_app_prod bash

# Run Aerich migrations manually in prod
prod-migrate:
	docker exec -it fastapi_app_prod aerich migrate

prod-upgrade:
	docker exec -it fastapi_app_prod aerich upgrade

# -------- CLEANUP --------
clean:
	docker system prune -f
	docker volume prune -f
