VENV := ./.venv
PIP := $(VENV)/bin/pip
PIP_COMPILE := $(VENV)/bin/pip-compile

PIP_SYNC := $(VENV)/bin/pip-sync

.PHONY: setup clean install-%

setup:
	virtualenv $(VENV) -p python3.12
	$(PIP) install pip-tools

install: 
	$(PIP_COMPILE) ./requirements/requirements.in ./requirements/requirements-dev.in -v --output-file ./requirements.txt
	$(PIP_SYNC) -v

check:
	$(PIP_COMPILE) --upgrade --dry-run  ./requirements/requirements.in ./requirements/requirements-dev.in -v

download-models:
	sanic server:bootstrap exec download_models

sync-db:
	sanic server:bootstrap exec sync_db

dev:
	GRAPHITI_TELEMETRY_ENABLED="false" TRANSFORMERS_OFFLINE="true" HF_DATASETS_OFFLINE="1" sanic server:bootstrap --factory --debug --host=0.0.0.0 --port=18082

test:
	pytest -n auto


build-base:
	docker build -t bklite/metis:base -f ./support-files/Dockerfile.base .
	docker push bklite/metis:base

release:
	docker build -t bklite/metis -f ./support-files/Dockerfile .
	docker push bklite/metis

