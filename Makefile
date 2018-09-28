DEV_LISTEN_IP := localhost
DEV_PORT := 3000
PIP_HOME = $(shell python3 -c "import site; import os; print(os.path.join(site.USER_BASE, 'bin'))" \
	|| python -c "import site; import os; print(os.path.join(site.USER_BASE, 'bin'))")

.PHONY: dev
dev:
	HKNWEB_MODE='dev' pipenv run python ./manage.py runserver $(DEV_LISTEN_IP):$(DEV_PORT)

.PHONY: dev-vagrant
dev-vagrant:
	HKNWEB_MODE='dev' pipenv run python ./manage.py runserver [::]:$(DEV_PORT)

.PHONY: livereload
livereload:
	pipenv run python ./manage.py livereload $(DEV_LISTEN_IP):$(DEV_PORT)


setup: pipenv venv migrate

.PHONY: pipenv
pipenv:
	pip3 install --user pipenv || pip install --user pipenv
	@echo Please add $(PIP_HOME) to your PATH variable.

.PHONY: venv
venv: Pipfile Pipfile.lock
	pipenv install --dev

.PHONY: migrate
migrate:
	pipenv run python ./manage.py migrate --settings=hknweb.settings.dev

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
