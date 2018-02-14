DEV_LISTEN_IP := localhost
DEV_PORT := 3000
PIP_HOME = $(shell python3 -c "import site; import os; print(os.path.join(site.USER_BASE, 'bin'))" \
	|| python -c "import site; import os; print(os.path.join(site.USER_BASE, 'bin'))")

.PHONY: dev
dev:
	@echo -e "\e[1m\e[93mRunning on http://${DEV_LISTEN_IP}:${DEV_PORT}/\e[0m"
	pipenv run python ./manage.py runserver ${DEV_LISTEN_IP}:${DEV_PORT}

setup: pipenv venv

.PHONY: pipenv
pipenv:
	pip install --user pipenv
	@echo Please add $(PIP_HOME) to your PATH variable.

.PHONY: venv
venv: Pipfile Pipfile.lock
	pipenv install --dev

.PHONY: clean
clean:
	pipenv --rm

.PHONY: update
update: venv
	pipenv update

