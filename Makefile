PYTHON ?= python3

.PHONY: format lint typecheck test evidence secrets quality

format:
	$(PYTHON) -m ruff format .

lint:
	$(PYTHON) -m ruff format --check .
	$(PYTHON) -m ruff check .

typecheck:
	$(PYTHON) -m mypy src

test:
	$(PYTHON) -m pytest

evidence:
	$(PYTHON) scripts/check_study.py studies/round1-cross-sectional-reversal

secrets:
	$(PYTHON) scripts/check_secrets.py

quality: lint typecheck test evidence secrets
