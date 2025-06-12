python manage.py migrate || true
python manage.py createcachetable django_cache
python manage.py collectstatic --noinput

echo "系统管理资源初始化..."
python manage.py init_realm_resource || true
python manage.py init_login_settings || true
python manage.py create_user admin password --email=admin@bklite.net --is_superuser || true

echo "CMDB资源初始化..."
python manage.py model_init || true

#echo "初始化访客角色..."
#python manage.py init_guest_role

echo "初始化监控资源..."
python manage.py plugin_init || true

echo "初始化节点管理..."
python manage.py node_init || true

supervisord -n