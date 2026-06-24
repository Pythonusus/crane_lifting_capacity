#!/bin/bash

# Exit on error
set -e

PORT="${VPS_PORT:-8102}"

# Logging functions
log() { echo "[$(date +'%H:%M:%S')] $1"; }
error() { echo "❌ $1"; exit 1; }
info() { echo "ℹ️ $1"; }

# Check if Docker is installed on host
command -v docker >/dev/null 2>&1 || error "Docker is not installed"

# Check if docker compose is installed on host
command -v docker compose >/dev/null 2>&1 || error "Docker Compose is not installed"

# Starting deploy
log "🚀 Deploy"

COMMIT_HASH=$(git rev-parse --short HEAD)
COMMIT_MESSAGE=$(git log -1 --pretty=%B)
COMMIT_AUTHOR=$(git log -1 --pretty=%an)

info "Commit: ${COMMIT_HASH}"
info "Author: ${COMMIT_AUTHOR}"
info "Message: ${COMMIT_MESSAGE}"

# Remove existing container if it exists
# Website will be unavailable for a few seconds until the new container is started
# --force-recreate is useless here, because we start new container from temporary directory
# --force-recreate recreates only containers from the same project
if docker container inspect "cranes-nginx" >/dev/null 2>&1; then
    log "♻️ Removing existing container cranes-nginx..."
    docker rm -f "cranes-nginx"
fi

if docker container inspect "cranes-backend" >/dev/null 2>&1; then
    log "♻️ Removing existing container cranes-backend..."
    docker rm -f "cranes-backend"
fi

# Starting new container
docker compose -f compose-VPS.yaml up -d --build

log "🏥 Healthcheck on port ${PORT} and backend /health endpoint..."
for i in $(seq 1 30); do

    FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:${PORT}" || true)
    BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:${PORT}/health" || true)

    if echo "${FRONTEND_STATUS}" | grep -q "200\|301\|302" && [ "${BACKEND_STATUS}" = "200" ]; then
        log "✅ Frontend is reachable and backend /health is healthy"
        break
    fi

    [ "$i" -eq 30 ] && error "Healthcheck failed (frontend: ${FRONTEND_STATUS}, backend /health: ${BACKEND_STATUS})"

    sleep 1
done

log "🧹 Cleaning up old images..."
docker image prune -f

log "🎉 Deployment completed!"
