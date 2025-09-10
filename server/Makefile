push:
	git add . && codegpt commit . && git push

install:
	uv sync --all-groups

migrate:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py createcachetable django_cache

server-init:
	python manage.py init_realm_resource
	python manage.py init_login_settings 
	python manage.py create_user admin password --email=admin@bklite.net --is_superuser 
	python manage.py model_init
	python manage.py plugin_init 
	python manage.py node_init
	python manage.py log_init
	python manage.py init_bot 
	python manage.py init_channel 
	python manage.py init_llm 
	python manage.py create_builtin_rules --update

setup-dev-user:
	DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_EMAIL=admin@example.com DJANGO_SUPERUSER_PASSWORD=password python manage.py createsuperuser --noinput

i18n:
	python manage.py makemessages -l zh_Hans
	python manage.py makemessages -l en
	python manage.py compilemessages

collect-static:
	python manage.py collectstatic --noinput

dev:
	uvicorn asgi:application --host 0.0.0.0 --port 8001 --reload --workers 1

run:
	gunicorn -w 4 -b 0.0.0.0:8001 asgi:application -k uvicorn.workers.UvicornWorker

clean-migrate:
	cd apps &&\
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete &&\
	find . -path "*/migrations/*.pyc"  -delete

init-buckets:
	python manage.py initialize_buckets

celery:
	celery -A apps.core.celery worker -B --loglevel=info --pool threads

celery-inspect:
	celery -A apps.core.celery inspect scheduled

celery-flower:
	celery -A apps.core.celery flower

start-nats:
	python manage.py nats_listener

test:
	pytest
