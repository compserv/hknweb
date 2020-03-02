PIP_HOME = $(shell python3 -c "import site; import os; print(os.path.join(site.USER_BASE, 'bin'))" \
	|| python -c "import site; import os; print(os.path.join(site.USER_BASE, 'bin'))")

IP ?= 127.0.0.1
PORT ?= 3000

.PHONY: dev
dev:
	HKNWEB_MODE='dev' pipenv run python ./manage.py runserver $(IP):$(PORT)

.PHONY: livereload
livereload:
	HKNWEB_MODE='dev' pipenv run python ./manage.py livereload $(IP):$(PORT)

setup: pipenv venv migrate

.PHONY: pipenv
pipenv:
	pip3 install --user pipenv || pip install --user pipenv
	@echo Please add $(PIP_HOME) to your PATH variable.

.PHONY: venv
venv: Pipfile Pipfile.lock
	pipenv install --dev

.PHONY: createsuperuser
createsuperuser:
	HKNWEB_MODE='dev' pipenv run python ./manage.py createsuperuser

.PHONY: superuser
createsuperuser:
	HKNWEB_MODE='dev' pipenv run python ./manage.py createsuperuser

.PHONY: migrate
migrate:
	HKNWEB_MODE='dev' pipenv run python ./manage.py migrate

.PHONY: makemigrations
makemigrations:
	HKNWEB_MODE='dev' pipenv run python ./manage.py makemigrations

.PHONY: migrations
migrations:
	HKNWEB_MODE='dev' pipenv run python ./manage.py makemigrations

.PHONY: test
test: venv
	pipenv run pytest -v tests/
	pipenv run pre-commit run --all-files

.PHONY: clean
clean:
	pipenv --rm

.PHONY: update
update: venv
	pipenv update

.PHONY: mysql
mysql:
	mysql -e "CREATE DATABASE IF NOT EXISTS hkn;"
	mysql -e "GRANT ALL PRIVILEGES ON hkn.* TO 'hkn'@'localhost' IDENTIFIED BY 'hknweb-dev';"
