check:
	pylint jsonator/ --disable=similarities || true
	pylint tests/ --disable=similarities || true
	@echo "========================================================================================="
	mypy --disallow-untyped-calls --disallow-untyped-defs --disallow-incomplete-defs --no-implicit-optional jsonator/ || true
	mypy --disallow-untyped-calls --disallow-untyped-defs --disallow-incomplete-defs --no-implicit-optional tests/ || true
	@echo "========================================================================================="
	isort --profile black --check-only jsonator/
	isort --profile black --check-only tests/
	@echo "========================================================================================="
	black --line-length=100 --target-version=py39 --target-version=py310 --target-version=py311 --check jsonator/
	black --line-length=100 --target-version=py39 --target-version=py310 --target-version=py311 --check tests/
format:
	isort --profile black jsonator/
	isort --profile black tests/
	@echo "========================================================================================="
	black --line-length=100 --target-version=py39 --target-version=py310 --target-version=py311 jsonator/
	black --line-length=100 --target-version=py39 --target-version=py310 --target-version=py311 tests/
test:
	pytest tests -vv
