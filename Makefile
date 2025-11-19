.PHONY: help install test run build push clean docker-run docker-stop

# Default target
help:
	@echo "Desifaces Image Service - Available commands:"
	@echo ""
	@echo "  make install      - Install Python dependencies"
	@echo "  make test         - Run tests"
	@echo "  make run          - Run the HTTP server locally"
	@echo "  make build        - Build Docker image"
	@echo "  make push         - Push Docker image to registry"
	@echo "  make docker-run   - Run the service in Docker"
	@echo "  make docker-stop  - Stop Docker containers"
	@echo "  make clean        - Clean temporary files"
	@echo ""

# Install dependencies
install:
	pip install -r requirements.txt

# Run tests
test:
	python3 test_service.py

# Run the HTTP server
run:
	python3 app.py

# Build Docker image
build:
	docker build -t desifaces-image-service:v2 .

# Push to Docker registry (customize with your registry)
push: build
	@echo "Please update the Makefile with your Docker registry details"
	@echo "Example: docker tag desifaces-image-service:v2 your-registry/desifaces-image-service:v2"
	@echo "         docker push your-registry/desifaces-image-service:v2"

# Run with docker-compose
docker-run:
	docker-compose up -d

# Stop docker-compose
docker-stop:
	docker-compose down

# Clean temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .pytest_cache/ htmlcov/ .coverage
