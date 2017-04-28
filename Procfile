release: python manage.py makemigrations auth contenttypes sessions messages staticfiles rest_framework rest_framework_swagger buyer vendor --noinput && python manage.py migrate
web: gunicorn picole.wsgi --log-file -
