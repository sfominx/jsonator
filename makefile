check:
	python3 -m pylint jsonator/ || true
	python3 -m pylint tests/ || true
	@echo "========================================================================================="
	python3 -m mypy --disallow-untyped-calls --disallow-untyped-defs --disallow-incomplete-defs --no-implicit-optional jsonator/ || true
	python3 -m mypy --disallow-untyped-calls --disallow-untyped-defs --disallow-incomplete-defs --no-implicit-optional tests/ || true
	@echo "========================================================================================="
	python3 -m isort --profile black --check-only jsonator/
	python3 -m isort --profile black --check-only tests/
	@echo "========================================================================================="
	python3 -m black --line-length=100 --target-version=py39 --target-version=py310 --target-version=py311 --check jsonator/
	python3 -m black --line-length=100 --target-version=py39 --target-version=py310 --target-version=py311 --check tests/
format:
	python3 -m isort --profile black jsonator/
	python3 -m isort --profile black tests/
	@echo "========================================================================================="
	python3 -m black --line-length=100 --target-version=py39 --target-version=py310 --target-version=py311 jsonator/
	python3 -m black --line-length=100 --target-version=py39 --target-version=py310 --target-version=py311 tests/
test:
	python3 -m pytest tests -vv
