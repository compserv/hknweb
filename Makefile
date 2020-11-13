PIP_HOME = $(shell python3 -c "import site; import os; print(os.path.join(site.USER_BASE, 'bin'))" \
	|| python -c "import site; import os; print(os.path.join(site.USER_BASE, 'bin'))")

IP ?= 127.0.0.1
PORT ?= 3000

.PHONY: dev
dev:
	HKNWEB_MODE='dev' python ./manage.py runserver $(IP):$(PORT)

.PHONY: livereload
livereload:
	HKNWEB_MODE='dev' python ./manage.py livereload $(IP):$(PORT)

.PHONY: setup
setup:
	python3 -m venv hknweb_dev
	# Left here as a reference :))
	# source hknweb_dev/bin/activate

.PHONY: install
install:
	python -m pip install --upgrade pip
	python -m pip install --upgrade setuptools
	python -m pip install -r requirements.txt

.PHONY: createsuperuser superuser
superuser: createsuperuser
createsuperuser:
	HKNWEB_MODE='dev' python ./manage.py createsuperuser

.PHONY: migrate
migrate:
	HKNWEB_MODE='dev' python ./manage.py migrate

.PHONY: makemigrations migrations
migrations: makemigrations
makemigrations:
	HKNWEB_MODE='dev' python ./manage.py makemigrations

.PHONY: shell
shell:
	HKNWEB_MODE='dev' python ./manage.py shell

.PHONY: test
test: venv
	pytest -v tests/
	pre-commit run --all-files

.PHONY: mysql
mysql:
	mysql -e "CREATE DATABASE IF NOT EXISTS hkn;"
	mysql -e "GRANT ALL PRIVILEGES ON hkn.* TO 'hkn'@'localhost' IDENTIFIED BY 'hknweb-dev';"

.PHONY: permissions
permissions:
	HKNWEB_MODE='dev' python ./manage.py shell < hknweb/init_permissions.py
