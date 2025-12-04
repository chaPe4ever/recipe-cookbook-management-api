# Procfile for deployment platforms (Render, Heroku, etc.)
# This file tells the platform how to run your application

# Web process - runs the Django application
web: gunicorn recipe_cookbok_management.wsgi:application --bind 0.0.0.0:$PORT

# Release process - runs migrations and collects static files before deployment
release: python manage.py migrate && python manage.py collectstatic --noinput