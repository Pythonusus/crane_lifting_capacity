# ================================================
# Frontend builder
# ================================================
FROM node:22-alpine AS frontend-builder

WORKDIR /app

# Copy dependency files first for better caching
COPY frontend/package.json frontend/package-lock.json ./frontend/

# Install dependencies
RUN cd frontend && npm ci

# Copy frontend code
COPY frontend/ ./frontend/

# Build frontend
RUN cd frontend && npm run build

# Delete everything except dist folder to minimize layer size
RUN find ./frontend -mindepth 1 -maxdepth 1 ! -name 'dist' -exec rm -rf {} +

# ================================================
# Backend builder
# ================================================
FROM python:3.13-alpine AS backend-builder

# Copy uv binary from official image (pinned to 0.8.11)
# No PATH modification needed as /usr/local/bin is in PATH by default
COPY --from=ghcr.io/astral-sh/uv:0.8.11 /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files first for better caching
COPY backend/pyproject.toml backend/uv.lock ./backend/

# Install backend production dependencies
RUN cd backend && uv sync --no-dev

# Copy backend code
COPY backend/ ./backend/

# ================================================
# Production image
# ================================================
FROM python:3.13-alpine AS crane-lifting-capacity-production

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Python logs appear in real time.
ENV PYTHONUNBUFFERED=1

# Copy uv binary from official image (pinned to 0.8.11)
# No PATH modification needed as /usr/local/bin is in PATH by default
COPY --from=ghcr.io/astral-sh/uv:0.8.11 /uv /usr/local/bin/uv

# Set working directory
WORKDIR /crane_lifting_capacity

# Copy installed packages and code from builder image
# Copy the .venv directory which contains installed packages
COPY --from=backend-builder /app/backend/.venv/ ./backend/.venv/
# Copy the app code
COPY --from=backend-builder /app/backend/app/ ./backend/app/
# Copy main.py and other necessary files
COPY --from=backend-builder /app/backend/main.py ./backend/
COPY --from=backend-builder /app/backend/utils ./backend/utils


# Copy frontend dist folder from builder image
COPY --from=frontend-builder /app/frontend/dist/ ./frontend/dist/

# Expose port (can be set with PORT environment variable)
# Default to 8000
EXPOSE ${PORT:-8000}

# Add non-root user in production stage
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup

# Change ownership of app directory
RUN chown -R appuser:appgroup /crane_lifting_capacity
USER appuser

# Directory that will be mounted as a volume via docker-compose
# Used to access prepopulated sqlite database
RUN mkdir -p data

# Create logs directory that will be mounted as a volume with 777 permissions
RUN mkdir -p logs && chmod 777 logs

# Run production server
CMD cd backend && uv run main.py
