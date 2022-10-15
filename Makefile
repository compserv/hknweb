CONDA_ENV := hknweb
PYTHON_VERSION := 3.7.3
PYTHON := python
MANAGE := HKNWEB_MODE='dev' $(PYTHON) ./manage.py

IP ?= 127.0.0.1
PORT ?= 3000

# This is REQUIRED on all makefile commands involving PYTHON or MANAGE
.PHONY: check-conda-env
check-conda-env:
ifeq ($(CONDA_PREFIX),)
	@echo "Conda Environment not detected. Please activate $(CONDA_ENV) Conda environment."
	exit 1
else ifneq ($(CONDA_DEFAULT_ENV), $(CONDA_ENV))
	@echo "Incorrect Conda Environment, should be $(CONDA_ENV). Currently is $(CONDA_DEFAULT_ENV)."
	exit 1
endif

.PHONY: dev
dev: check-conda-env
	$(MANAGE) runserver $(IP):$(PORT)

.PHONY: livereload
livereload: check-conda-env
	$(MANAGE) livereload $(IP):$(PORT)

.PHONY: conda-scratch
conda-scratch:
	# Makes hknweb environment from scratch (overwriting old one if exists)
	conda create -n $(CONDA_ENV) python=$(PYTHON_VERSION) -y
	@echo "When developing, activate the $(CONDA_ENV) Conda environment with 'conda activate $(CONDA_ENV)' so Python can access the installed dependencies."

.PHONY: conda
conda:
	@# We don't use "-y" because if environment recrated, it will destroy and reinstall ... since it is an all "yes"
	@#  Just confirm to the default options (option given is: Yes install OR, if created already, No remove and reinstall)
	echo -e "\n" | conda create -n $(CONDA_ENV) python=$(PYTHON_VERSION)
	@echo "When developing, activate the $(CONDA_ENV) Conda environment with 'conda activate $(CONDA_ENV)' so Python can access the installed dependencies."

# Installs dependencies for Development and Production only
#  shared between "install-prod" and "install"
.PHONY: install-common
install-common: check-conda-env
	$(PYTHON) -m pip install --upgrade pip setuptools
	$(PYTHON) -m pip install -r requirements.txt

# Installs dependencies for Production only
.PHONY: install-prod
install-prod: check-conda-env
	make install-common
	$(PYTHON) -m pip install -r requirements-prod.txt

# Installs dependencies for Development only
.PHONY: install
install: check-conda-env
	make install-common
	$(PYTHON) -m pip install -r requirements-dev.txt

.PHONY: createsuperuser superuser
superuser: createsuperuser
createsuperuser: check-conda-env
	$(MANAGE) createsuperuser

.PHONY: migrate
migrate: check-conda-env
	$(MANAGE) migrate

.PHONY: makemigrations migrations
migrations: makemigrations
makemigrations: check-conda-env
	$(MANAGE) makemigrations

.PHONY: shell
shell: check-conda-env
	$(MANAGE) shell

.PHONY: test
test: conda
	make check-conda-env
	HKNWEB_MODE='dev' coverage run --source='.' ./manage.py test --pattern="test_*.py"
	coverage report --skip-covered --omit=deploy*,fabfile.py,hknweb/wsgi.py,manage.py,*apps.py,*test_*.py,hknweb/settings/*.py --sort=miss --fail-under=80

.PHONY: clean
clean:
	conda env remove -n $(CONDA_ENV)

.PHONY: mysql
mysql:
	mysql -e "CREATE DATABASE IF NOT EXISTS hkn;"
	mysql -e "GRANT ALL PRIVILEGES ON hkn.* TO 'hkn'@'localhost' IDENTIFIED BY 'hknweb-dev';"

.PHONY: permissions
permissions: check-conda-env
	$(MANAGE) shell -c "from hknweb.init_permissions import provision; provision()"

.PHONY: format
format: check-conda-env
	$(PYTHON) -m black . --exclude "/(.*migrations)/"
