CONDA_ENV := hknweb
PYTHON_VERSION := 3.7.3
PYTHON := python
MANAGE := HKNWEB_MODE='dev' $(PYTHON) ./manage.py

IP ?= 127.0.0.1
PORT ?= 3000

.PHONY: dev
dev:
	$(MANAGE) runserver $(IP):$(PORT)

.PHONY: livereload
livereload:
	$(MANAGE) livereload $(IP):$(PORT)

.PHONY: conda
conda:
	# We don't use "-y" because if environment recrated, it will destroy and reinstall ... since it is an all "yes"
	#  Just default to the default options (option given is either: Yes install OR No remove and reinstall)
	echo -e "\n" | conda create -n $(CONDA_ENV) python=$(PYTHON_VERSION) -q
	@echo "When developing, activate the HKNWeb Conda environment with 'conda activate $(CONDA_ENV)' so Python can access the installed dependencies."

# Installs dependencies for Development and Production only
#  shared between "install-prod" and "install"
.PHONY: install-common
install-common:
	$(PYTHON) -m pip install --upgrade pip setuptools
	# TODO: pinned/unpinned dependency version.
	#  It's also usually useful to have a place where they're pinned (like they are here)
	#  with all dependencies pinned too, and then have a place for the actual looser
	#  requirements directly needed for the app (django for instance, but not specifying a
	#  version unless there's compatibility problems),
	#  this makes it much easier to be able to upgrade and know why things are pinned.
	$(PYTHON) -m pip install -r requirements.txt

# Installs dependencies for Production only
.PHONY: install-prod
install-prod:
	make install-common
	$(PYTHON) -m pip install -r requirements-prod.txt

# Installs dependencies for Development only
.PHONY: install
install:
	make install-common
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
test: conda
	HKNWEB_MODE='dev' coverage run --source='.' ./manage.py test --pattern="test_*.py"
	coverage report --skip-covered --omit=deploy*,fabfile.py,hknweb/wsgi.py,manage.py,*apps.py,*test_*.py,hknweb/settings/*.py --sort=miss --fail-under=80

.PHONY: clean
clean:
	conda env remove -n hknweb

.PHONY: mysql
mysql:
	mysql -e "CREATE DATABASE IF NOT EXISTS hkn;"
	mysql -e "GRANT ALL PRIVILEGES ON hkn.* TO 'hkn'@'localhost' IDENTIFIED BY 'hknweb-dev';"

.PHONY: permissions
permissions:
	$(MANAGE) shell -c "from hknweb.init_permissions import provision; provision()"

.PHONY: format
format:
	$(PYTHON) -m black . --exclude "/(.*migrations|\.venv)/"
