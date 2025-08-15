# All commands are assumed to be run from the root of the project

# ===== COMMON =====

# Install pre-commit hooks
pre-commit-install:
	cd backend && uv run pre-commit install

# Run pre-commit hooks
pre-commit:
	cd backend && uv run pre-commit run --all-files


# ===== BACKEND =====

# Install prod and dev dependencies using uv package manager
install-backend-dev:
	cd backend && uv sync

# Install prod dependencies using uv package manager
install-backend-prod:
	cd backend && uv sync --no-dev

# Run ruff linter on backend app with config from pyproject.toml
lint-backend:
	cd backend && uv run ruff check --config pyproject.toml app

# Format backend app with config from pyproject.toml
format-backend:
	cd backend && uv run ruff check --config pyproject.toml --fix app

# Create a new migration
# Usage: make create-migration m="Add new column to table"
create-migration:
	cd backend && uv run alembic revision --autogenerate -m "$(m)"

# Apply all pending migrations
migrate:
	cd backend && uv run alembic upgrade head

# Populate database from Excel files. Paths are taken from .env file.
populate-db:
	cd backend && uv run python manage.py populate-db

# Dump cranes data to JSON files in cranes_dump directory
dump-cranes:
	cd backend && uv run python manage.py dump-cranes

# Print cranes summary only (no JSON files)
show-cranes-summary:
	cd backend && uv run python manage.py show-cranes-summary

# Dump cranes data to custom directory
dump-cranes-custom:
	cd backend && uv run python manage.py dump-cranes --output-dir "$(dir)"

# Run pytest on backend app with verbose test output
test-backend:
	cd backend && DEVELOPMENT=true uv run pytest -vv

# Run pytest on backend app with coverage report. Generate html and xml reports.
# Also shows terminal report. No report is generated if tests fail.
test-backend-coverage:
	cd backend && DEVELOPMENT=true uv run pytest \
		--cov=app \
		--cov-config=pyproject.toml \
		--cov-report=html \
		--cov-report=xml \
		--cov-report=term \
		--no-cov-on-fail

# Start backend server in dev mode.
# PYTHONPATH is needed because fastapi cli doesn't add the current directory to the PYTHONPATH automatically.
start-backend-dev:
	cd backend && PYTHONPATH=. uv run fastapi dev app/api.py

# Start backend server in prod mode.
# No PYTHONPATH is needed because direct script execution automatically adds the script's directory to the PYTHONPATH.
start-backend:
	cd backend && uv run main.py


# ===== FRONTEND =====

# Install dev and prod dependencies
install-frontend-dev:
	cd frontend && npm ci

# Install prod dependencies
install-frontend-prod:
	cd frontend && npm ci --production

# Build frontend for production
build-frontend:
	cd frontend && npm run build

# Lint frontend code using eslint and prettier
lint-frontend:
	cd frontend && npm run lint

# Fix linting issues in frontend code
format-frontend:
	cd frontend && npm run lint:fix

# Run frontend tests
test-frontend:
	cd frontend && npm run test

# Run frontend tests in watch mode
test-frontend-watch:
	cd frontend && npm run test:watch

# Run frontend tests with coverage report
test-frontend-coverage:
	cd frontend && npm run test:coverage

# Preview production build
preview-frontend:
	cd frontend && npm run preview

# Start frontend in development mode
start-frontend-dev:
	cd frontend && npm run dev


# ===== DOCKER =====

# Build all services
docker-build:
	docker compose build

# Start all services
docker-start:
	docker compose up

# Stop all services
docker-stop:
	docker compose stop

# Stop and remove all services
docker-down:
	docker compose down

# Start sh session inside the container
# Using sh instead of bash because alpine doesn't have bash by default
docker-shell:
	docker compose exec crane-lifting-capacity-production sh

.PHONY: pre-commit-install pre-commit \
        install-backend-dev install-backend-prod lint-backend format-backend test-backend \
        start-backend-dev start-backend populate-db dump-cranes dump-cranes-with-attachments \
        dump-cranes-summary dump-cranes-custom \
        install-frontend-dev install-frontend-prod build-frontend lint-frontend \
        format-frontend test-frontend test-frontend-watch test-frontend-coverage \
        preview-frontend start-frontend-dev \
				docker-build docker-start docker-stop docker-down docker-shell
