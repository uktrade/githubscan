web: python manage.py collectstatic & & python manage.py migrate - -noinput & & gunicorn config.wsgi: application - -bind 0.0.0.0: $PORT - -timeout 300 - -log-file -
