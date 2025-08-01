# Project Setup and Usage

## I. First-Time Setup
1. Start dev environment:  
   ```bash
   make dev-up

2. Initialize database migrations (only first time):
   See VI. Migrations

## II. Development Environment
The development environment is designed for hot-reload, local folder sync, and easy schema updates.

| Command            | Description                                                                    |
| ------------------ | ------------------------------------------------------------------------------ |
| `make dev-up`      | Start the development containers with hot-reload and bind-mounted local files. |
| `make dev-down`    | Stop and remove dev containers.                                                |
| `make dev-logs`    | View live logs from dev containers.                                            |
| `make dev-bash`    | Enter the dev app container shell (bash).                                      |
| `make dev-migrate` | Generate new Aerich migrations after you modify models.                        |
| `make dev-upgrade` | Apply database migrations to the dev database.                                 |

## III. Production Environment
The production environment builds immutable Docker images, no live file sync.

| Command            | Description                                                                          |
| ------------------ |--------------------------------------------------------------------------------------|
| `make prod-up`      | Start the production containers in detached mode.                                    |
| `make prod-down`    | Stop and remove prod containers.                                                     |
| `make prod-logs`    | View logs from the production containers.                                            |
| `make prod-bash`    | Enter the production app container shell (bash).                                     |
| `make prod-migrate` | Generate Aerich migrations in the production container (recommended to do manually). |
| `make prod-upgrade` | Apply migrations in production.                                                      |

| Command             | Description                                                                          |
| ------------------- | ------------------------------------------------------------------------------------ |
| `make prod-up`      | Start the production containers in detached mode.                                    |
| `make prod-down`    | Stop and remove prod containers.                                                     |
| `make prod-logs`    | View logs from the production containers.                                            |
| `make prod-bash`    | Enter the production app container shell (bash).                                     |
| `make prod-migrate` | Generate Aerich migrations in the production container (recommended to do manually). |
| `make prod-upgrade` | Apply migrations in production.                                                      |

## IV. Cleanup Commands
```bash
make clean
```   
   

## V. API Documentation
Once the app is running:

http://localhost:8000/docs – Interactive Swagger API docs.

## VI. Migrations
### Core Database
```bash
aerich init -t app.db.core.TORTOISE_ORM_CORE --location ./migrations_core
aerich init-db
aerich migrate --name add_some_field_to_core
aerich upgrade
```

### Tenant Databases
aerich init -t app.db.tenant.TORTOISE_ORM_TENANT --location ./migrations_tenant
aerich init-db
aerich migrate --name add_some_field_to_core
aerich upgrade

or

```bash
python migrate_tenants.py
```

## Monitoring Tools
### RabbitMQ UI
http://localhost:15672
### Celery Flower
http://localhost:5555
### RedisInsight
http://localhost:8001
