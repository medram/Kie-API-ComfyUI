.PHONY: help format lint typecheck clean

.DEFAULT_GOAL := help

typecheck:
	uv --project ./kie_nodes run mypy --config-file ./kie_nodes/pyproject.toml .

format:
	uv --project ./kie_nodes run ruff format .

lint:
	uv --project ./kie_nodes run ruff check --fix .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✓ Cleaned cache and compiled files"


help:
	@echo "Available targets:"
	@echo "  typecheck  - Run mypy for type checking"
	@echo "  format     - Format code using ruff"
	@echo "  lint       - Lint code using ruff and fix issues"
	@echo "  clean      - Remove __pycache__ directories and .pyc files"