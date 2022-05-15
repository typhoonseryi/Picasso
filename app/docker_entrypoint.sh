sleep 1
python manage.py migrate
python etl/etl.py &
gunicorn config.wsgi:application -b 0.0.0.0:8000
