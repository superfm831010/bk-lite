python manage.py migrate
python manage.py createcachetable django_cache
python manage.py collectstatic --noinput

python manage.py init_realm_resource
python manage.py init_login_settings
python manage.py create_user admin password --email=admin@bklite.net --is_superuser || true

supervisord -n