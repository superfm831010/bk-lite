push:
	git add . && codegpt commit . && git push

clean:
	rm -Rf ./dist

setup:
	virtualenv .venv -p python3.10
	./.venv/bin/pip install pip-tools


install:
	./.venv/bin/pip-compile ./requirements/requirements-core.txt \
							./requirements/requirements-extra.txt \
						-v --output-file ./requirements.txt
	./.venv/bin/pip-sync -v

install-hook:
	pre-commit install

lint:
	pre-commit run --all-files

run:
	sanic server:app --host=0.0.0.0 --port=8083 --workers=1

build:
	docker build -t bklite/stargazer -f ./support-files/docker/Dockerfile .