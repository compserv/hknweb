PIP_HOME = $(shell python3 -c "import site; import os; print(os.path.join(site.USER_BASE, 'bin'))" \
	|| python -c "import site; import os; print(os.path.join(site.USER_BASE, 'bin'))")

VENV := .venv
BIN := $(VENV)/bin
PYTHON := $(BIN)/python
MANAGE := HKNWEB_MODE='dev' $(PYTHON) ./manage.py
BREW_DIR := $(shell brew --prefix)

IP ?= 127.0.0.1
PORT ?= 3000

.PHONY: dev
dev:
	$(MANAGE) runserver $(IP):$(PORT)

.PHONY: livereload
livereload:
	$(MANAGE) livereload $(IP):$(PORT)

.PHONY: venv
venv:
	python3 -m venv $(VENV)
	@echo "When developing, activate the virtualenv with 'source .venv/bin/activate' so Python can access the installed dependencies."

.PHONY: dependencies-macbook
dependencies-macbook:
	# Requirements: Homebrew (https://brew.sh/)
	brew install mysql

.PHONY: install-macbook
install-macbook:
	# Run dependencies-macbook first if you haven't already
	
	# https://stackoverflow.com/questions/67767255/error-when-install-mysqlclient-using-pip-to-macos-bigsur
	export LDFLAGS='-L${BREW_DIR}/lib -L${BREW_DIR}/opt/openssl/lib'
	export CPPFLAGS='-I${BREW_DIR}/include -I${BREW_DIR}/opt/openssl/include'

	make install

.PHONY: install-prod
install-prod:
	# Installs dependencies for Production only

	# For issues with binary packages, consider https://pythonwheels.com/
	# For destination production machine, "make install" should have
	#  upgraded already and it should detect and move on for "pip"
	$(PYTHON) -m pip install --upgrade pip setuptools

	# NOTE: If pip and setuptools is broken, use the following two lines
	#       and then commenting the two line above
	# $(PYTHON) -m pip install --upgrade "pip<=20.3.4"
	# $(PYTHON) -m pip install --upgrade "setuptools<=51.2.0"

	# TODO: pinned/unpinned dependency version.
	# See https://hkn-mu.atlassian.net/browse/COMPSERV-110
	$(PYTHON) -m pip install -r requirements.txt

.PHONY: install
install:
	# Installs dependencies for Development and Production

	# See:
	#  - https://github.com/compserv/hknweb/pull/272
	#  - https://github.com/compserv/hknweb/commit/cf826d4
	#  - https://github.com/compserv/hknweb/commit/124b108
	#  - https://github.com/hashicorp/vagrant/issues/12057
	# This is mainly a Vagrant workaround to allow pip upgrade
	$(PYTHON) -m pip install --upgrade pip setuptools --ignore-installed

	make install-prod
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
	$(MANAGE) test $(test_app)

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
