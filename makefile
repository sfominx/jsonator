check:
	pylint jsonator/ tests/ || true
	@echo "========================================================================================="
	mypy jsonator/ tests/ || true
	@echo "========================================================================================="
	isort --check-only jsonator/ tests/
	@echo "========================================================================================="
	black --check jsonator/ tests/

format:
	isort --profile black jsonator/ tests/
	@echo "========================================================================================="
	black jsonator/ tests/

test:
	pytest tests -vv
