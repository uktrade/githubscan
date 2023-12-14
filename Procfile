web: python manage.py collectstatic && python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --timeout 600 --log-file -
worker: celery -A config worker -l info
