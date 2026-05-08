release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
web: python manage.py migrate --noinput && gunicorn clyra.wsgi --bind 0.0.0.0:$PORT --access-logfile - --error-logfile -
