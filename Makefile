DEV_LISTEN_IP := localhost
DEV_PORT := 3000
PIP_HOME := $(shell python -c "import site; import os; print(os.path.join(site.USER_BASE, 'bin'))")

.PHONY: dev
dev: venv serve

setup:
	pip install --user pipenv > /dev/null
	@echo "Please add $(PIP_HOME) to your PATH variable."

venv: Pipfile Pipfile.lock
	pipenv install --dev

serve: venv
	@echo -e "\e[1m\e[93mRunning on http://$(DEV_LISTEN_IP):$(DEV_PORT)/\e[0m"
	pipenv run python ./manage.py runserver $(DEV_LISTEN_IP):$(DEV_PORT)

clean:
	pipenv --rm

update: venv
	pipenv update
