.PHONY: help install run-ui run-cli test docker-build docker-up clean

help:
	@echo "Available commands:"
	@echo "  make install       Install dependencies from requirements.txt"
	@echo "  make run-ui        Launch Streamlit web application"
	@echo "  make run-cli       Run command-line research pipeline"
	@echo "  make check         Verify Python syntax of all source files"
	@echo "  make docker-build  Build Docker image"
	@echo "  make docker-up     Run application via Docker Compose"
	@echo "  make clean         Remove Python bytecode and caches"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

run-ui:
	streamlit run app.py

run-cli:
	python pipeline.py

check:
	python -m py_compile agents.py app.py pipeline.py tools.py

docker-build:
	docker compose build

docker-up:
	docker compose up

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
