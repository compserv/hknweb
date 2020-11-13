PIP_HOME = $(shell python3 -c "import site; import os; print(os.path.join(site.USER_BASE, 'bin'))" \
	|| python -c "import site; import os; print(os.path.join(site.USER_BASE, 'bin'))")

BIN := .venv/bin
PYTHON := $(BIN)/python

IP ?= 127.0.0.1
PORT ?= 3000

.PHONY: dev
dev:
	HKNWEB_MODE='dev' $(PYTHON) ./manage.py runserver $(IP):$(PORT)

.PHONY: livereload
livereload:
	HKNWEB_MODE='dev' $(PYTHON) ./manage.py livereload $(IP):$(PORT)

.PHONY: setup
setup:
	python3 -m venv .venv
	@echo "When developing, activate the virtualenv with 'source hknweb_dev/bin/activate' so Python can access the installed dependencies."

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
	HKNWEB_MODE='dev' $(PYTHON) ./manage.py createsuperuser

.PHONY: migrate
migrate:
	HKNWEB_MODE='dev' $(PYTHON) ./manage.py migrate

.PHONY: makemigrations migrations
migrations: makemigrations
makemigrations:
	HKNWEB_MODE='dev' $(PYTHON) ./manage.py makemigrations

.PHONY: shell
shell:
	HKNWEB_MODE='dev' $(PYTHON) ./manage.py shell

.PHONY: test
test: venv
	pytest -v tests/
	pre-commit run --all-files

.PHONY: clean
clean:
	rm -rf .venv

.PHONY: mysql
mysql:
	mysql -e "CREATE DATABASE IF NOT EXISTS hkn;"
	mysql -e "GRANT ALL PRIVILEGES ON hkn.* TO 'hkn'@'localhost' IDENTIFIED BY 'hknweb-dev';"

.PHONY: permissions
permissions:
	HKNWEB_MODE='dev' $(PYTHON) ./manage.py shell < hknweb/init_permissions.py
