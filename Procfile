# Procfile for deployment platforms (Render, Heroku, etc.)
# This file tells the platform how to run your application

# Web process - runs the Django application
web: gunicorn recipe_cookbok_management.wsgi:application --bind 0.0.0.0:$PORT

# Release process - runs migrations and collects static files before deployment
# Note: If release command doesn't run on Render, add collectstatic to Build Command in dashboard
# Creates schema if DB_SCHEMA is set, then runs migrations
release: python manage.py create_schema && python manage.py migrate && python manage.py collectstatic --noinput