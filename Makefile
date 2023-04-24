#* Variables
SHELL := /usr/bin/env bash
PYTHON := python

#* Directories with source code
CODE = core

#* Include environment variables if .env exists
ifneq ("$(wildcard .env)","")
	include .env
	export
endif

#* Poetry
.PHONY: poetry-download
poetry-download:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | $(PYTHON) -

#* Installation
.PHONY: install
install:
	poetry install -n
	poetry run mypy --install-types --non-interactive $(CODE)
	pre-commit install

.PHONY: check-mypy
check-mypy:
	mypy --config-file pyproject.toml $(CODE)

#* Formatters
.PHONY: codestyle
codestyle:
	pyupgrade --exit-zero-even-if-changed --py39-plus **/*.py
	autoflake --recursive --in-place --remove-all-unused-imports --ignore-init-module-imports $(CODE)
	isort --settings-path pyproject.toml $(CODE)
	black --config pyproject.toml $(CODE)


#* Run
.PHONY: run
run:
	poetry run python3 -m core
