.PHONY: check
check:
	black --check .
	ruff check .
	mypy .

.PHONY: format
format:
	black .
	ruff check --fix .

.PHONY: test
test: check
	pytest
