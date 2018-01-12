DEV_LISTEN_IP := 0.0.0.0
DEV_PORT := 3000

.PHONY: dev
dev: venv serve

venv: Pipfile Pipfile.lock
	pipenv install --dev

serve:
	@echo -e "\e[1m\e[93mRunning on http://localhost:$(DEV_PORT)/\e[0m"
	pipenv run python ./manage.py runserver $(DEV_LISTEN_IP):$(DEV_PORT)

clean:
	pipenv uninstall --all --rm

update: venv
	pipenv update
