python manage.py migrate
python manage.py createcachetable django_cache
python manage.py collectstatic --noinput

#python manage.py init_guest_role

supervisord -n