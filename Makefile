ifeq ($(OS),Windows_NT)
	DETECTED_OS := Windows
else
	DETECTED_OS := $(shell uname)
endif

ENV := $(CURDIR)/.venv

ifeq ($(DETECTED_OS),Windows)
	BIN := $(ENV)/Scripts
else
	BIN := $(ENV)/bin
endif

PYTHON := $(BIN)/python
PIPENV_RUN := pipenv run
FLAKE8 := $(BIN)/flake8
COVERAGE := $(BIN)/coverage
NOSE2 := $(BIN)/nose2

export PIPENV_VENV_IN_PROJECT=1


help: ## This play the help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-38s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

install: ## Install dependencies for production
	pipenv install

install-dev: ## Install dependencies for development
	pipenv install --dev

lint: ## Run code linter
	$(FLAKE8)

test: ## Run all the tests
	$(NOSE2)

clean: ## Removes .venv folder and __pycache__ files
	rm -rf $(ENV)
	find . -name __pycache__ -type d -exec rm -rf {} \;

.PHONY: help install install-dev lint test clean
