PIP_HOME = $(shell python3 -c "import site; import os; print(os.path.join(site.USER_BASE, 'bin'))" \
	|| python -c "import site; import os; print(os.path.join(site.USER_BASE, 'bin'))")

VENV := .venv
BIN := $(VENV)/bin
PYTHON := $(BIN)/python
MANAGE := HKNWEB_MODE='dev' $(PYTHON) ./manage.py

IP ?= 127.0.0.1
PORT ?= 3000

.PHONY: dev
dev:
	$(MANAGE) runserver $(IP):$(PORT)

.PHONY: livereload
livereload:
	$(MANAGE) livereload $(IP):$(PORT)

.PHONY: setup
setup:
	python3 -m venv $(VENV)
	@echo "When developing, activate the virtualenv with 'source .venv/bin/activate' so Python can access the installed dependencies."

.PHONY: install
install:
	$(PYTHON) -m pip install --upgrade pip
	# For issues with binary packages, consider https://pythonwheels.com/
	$(PYTHON) -m pip install --upgrade setuptools
	# TODO: pinned/unpinned dependency version.
	# See https://github.com/compserv/hknweb/pull/272/files?file-filters%5B%5D=.html&file-filters%5B%5D=.md&file-filters%5B%5D=.py&file-filters%5B%5D=.txt&file-filters%5B%5D=.yml&file-filters%5B%5D=dotfile&hide-deleted-files=true&file-filters%5B%5D=.lock#r522718859
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install -r requirements-dev.txt

.PHONY: createsuperuser superuser
superuser: createsuperuser
createsuperuser:
	$(MANAGE) createsuperuser

.PHONY: migrate
migrate:
	$(MANAGE) migrate

.PHONY: makemigrations migrations
migrations: makemigrations
makemigrations:
	$(MANAGE) makemigrations

.PHONY: shell
shell:
	$(MANAGE) shell

.PHONY: test
test: venv
	pytest -v tests/
	pre-commit run --all-files

.PHONY: clean
clean:
	rm -rf $(VENV)

.PHONY: mysql
mysql:
	mysql -e "CREATE DATABASE IF NOT EXISTS hkn;"
	mysql -e "GRANT ALL PRIVILEGES ON hkn.* TO 'hkn'@'localhost' IDENTIFIED BY 'hknweb-dev';"

.PHONY: permissions
permissions:
	$(MANAGE) shell < hknweb/init_permissions.py
