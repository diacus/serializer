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
COVERAGE := $(BIN)/coverage

export PIPENV_VENV_IN_PROJECT=1


help: ## This play the help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-38s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

install: ## Install dependencies for production
	pipenv install

install-dev: tags ## Install dependencies for development
	pipenv install --dev

install-sys: ## Install the package
	pip3 install --upgrade .

clean-sys: ## Uninstall the package
	pip3 uninstall -y serializer

lint: ## Run code linter
	$(PIPENV_RUN) flake8 serializer test

test: ## Run all the tests
	$(PIPENV_RUN) nose2

tags: ## Run exuberant ctags
	ctags --exclude=.venv --exclude=.git -R .

shell:
	$(PIPENV_RUN) ptpython

clean: ## Removes .venv folder and __pycache__ files
	rm -rf $(ENV) tags
	find . -name __pycache__ -type d -exec rm -rf {} \;

.PHONY: clean help install install-dev lint shell tags test
