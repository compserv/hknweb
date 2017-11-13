BIN := venv/bin
PYTHON := $(BIN)/python
DEV_LISTEN_IP := 0.0.0.0
DEV_PORT := 3000

.PHONY: dev
dev: venv
	@echo -e "\e[1m\e[93mRunning on http://$(shell hostname -f):$(DEV_PORT)/\e[0m"
	$(PYTHON) ./manage.py runserver $(DEV_LISTEN_IP):$(DEV_PORT)

venv: requirements.txt requirements-dev.txt
	python ./vendor/venv-update venv= venv -ppython3 install= \
		-r requirements.txt -r requirements-dev.txt

.PHONY: clean
clean:
	rm -rf venv

.PHONY: update-requirements
update-requirements: venv
	$(BIN)/upgrade-requirements
