# ==========================================
# Pose2Pose PoC - Makefile
# ==========================================

.PHONY: help setup install-uv sync lock lock-check lock-upgrade update check-outdated \
        dev run test clean docker-build docker-up docker-down docker-logs docker-restart

# ==========================================
# Help
# ==========================================
help:
	@echo "Pose2Pose PoC - Available Commands"
	@echo "======================================"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup              - Complete setup for new developers"
	@echo "  make install-uv         - Install uv package manager"
	@echo ""
	@echo "Dependency Management:"
	@echo "  make sync               - Sync dependencies"
	@echo "  make lock               - Update uv.lock file"
	@echo "  make lock-check         - Check if uv.lock is up to date"
	@echo "  make lock-upgrade       - Upgrade all dependencies"
	@echo "  make update             - Update dependencies (alias)"
	@echo "  make check-outdated     - Check for outdated packages"
	@echo ""
	@echo "Development:"
	@echo "  make dev                - Run application locally"
	@echo "  make run                - Run application (alias for dev)"
	@echo "  make test               - Test backend functions"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build       - Build Docker image"
	@echo "  make docker-up          - Start the application"
	@echo "  make docker-down        - Stop the application"
	@echo "  make docker-restart     - Restart the application"
	@echo "  make docker-logs        - View application logs"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean              - Clean caches and generated files"
	@echo "  make help               - Show this help message"

# ==========================================
# Setup & Installation
# ==========================================

## Initial setup for local development
setup: install-uv
	@echo "Setting up Pose2Pose PoC..."
	@echo "Syncing dependencies..."
	uv sync --no-install-project
	@if [ ! -f .env ]; then \
		echo "Creating .env file..."; \
		echo "ENVIRONMENT=development" > .env; \
		echo "STREAMLIT_SERVER_PORT=8501" >> .env; \
		echo ".env file created"; \
	else \
		echo ".env file already exists"; \
	fi
	@echo ""
	@echo "✅ Setup complete! Run 'make dev' to start"

## Install uv package manager
install-uv:
	@echo "Checking for uv package manager..."
	@command -v uv >/dev/null 2>&1 || { \
		echo "uv not found. Installing..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	}
	@echo "✅ uv is installed"

# ==========================================
# Dependency Management
# ==========================================

## Sync dependencies
sync:
	@echo "Syncing dependencies..."
	uv sync --no-install-project
	@echo "✅ Dependencies synced"

## Update uv.lock file without upgrading
lock:
	@echo "Updating uv.lock file..."
	uv lock
	@echo "✅ Lockfile updated"

## Check if uv.lock is up to date
lock-check:
	@echo "Checking if uv.lock is up to date..."
	uv lock --check

## Upgrade all dependencies to latest versions
lock-upgrade:
	@echo "Upgrading all dependencies..."
	uv lock --upgrade
	uv sync --no-install-project
	@echo "✅ Dependencies upgraded and synced"
	@echo "⚠️  Check uv.lock and update pyproject.toml if needed!"

## Update dependencies (alias for lock-upgrade)
update: lock-upgrade

## Check for outdated packages
check-outdated:
	@echo "Checking for outdated packages..."
	uv pip list --outdated

# ==========================================
# Development Commands
# ==========================================

## Run application locally with Streamlit
dev:
	@echo "Starting Streamlit application..."
	@echo "URL: http://localhost:8501"
	@echo ""
	cd frontend && uv run streamlit run app.py

## Alias for dev
run: dev

## Test backend functions
test:
	@echo "Testing backend functions..."
	cd backend && uv run python main.py

# ==========================================
# Docker Commands
# ==========================================

## Build Docker image
docker-build:
	@echo "Building Docker image..."
	docker-compose build

## Start application with Docker
docker-up:
	@echo "Starting application with Docker..."
	@echo "URL: http://localhost:8501"
	docker-compose up -d

## Stop application
docker-down:
	@echo "Stopping application..."
	docker-compose down

## Restart application
docker-restart: docker-down docker-up

## View application logs
docker-logs:
	@echo "Viewing application logs..."
	docker-compose logs -f

# ==========================================
# Utilities
# ==========================================

## Clean generated files and caches
clean:
	@echo "Cleaning generated files and caches..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	rm -rf build/ dist/ .eggs/ .mypy_cache/
	@echo "✅ Clean complete"
