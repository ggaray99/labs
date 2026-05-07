release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
web: gunicorn clyra.wsgi --bind 0.0.0.0:$PORT
