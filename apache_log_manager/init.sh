python3 apache_log_manager/manage.py migrate

DJANGO_SUPERUSER_USERNAME=admin DJANGO_SUPERUSER_PASSWORD=123456 \
  python3 apache_log_manager/manage.py createsuperuser --email admin@example.com --noinput
