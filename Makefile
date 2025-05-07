# All commands are assumed to be run from the root of the project

# ===== COMMON =====

# Install pre-commit hooks
pre-commit-install:
	pre-commit install

# Run pre-commit hooks
pre-commit:
	pre-commit run --all-files


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

# Run pytest on backend app with verbose test output
test-backend:
	cd backend && uv run pytest -vv

# Run pytest on backend app with coverage report. Generate html and xml reports.
# Also shows terminal report. No report is generated if tests fail.
test-backend-coverage:
	cd backend && uv run pytest \
		--cov=app \
		--cov-config=pyproject.toml \
		--cov-report=html \
		--cov-report=xml \
		--cov-report=term \
		--no-cov-on-fail

# Start backend server in dev mode.
# PYTHONPATH is needed because fastapi cli doesn't add the current directory to the PYTHONPATH automatically.
start-backend-dev:
	cd backend && PYTHONPATH=. uv run fastapi dev app/server.py

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

.PHONY: pre-commit-install pre-commit \
        install-backend-dev install-backend-prod lint-backend format-backend test-backend \
        start-backend-dev start-backend \
        install-frontend-dev install-frontend-prod build-frontend lint-frontend \
        format-frontend test-frontend test-frontend-watch test-frontend-coverage \
        preview-frontend start-frontend-dev
