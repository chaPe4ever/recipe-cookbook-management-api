#!/bin/bash
# Build script for Render deployment
# This ensures static files are collected during build

set -o errexit  # Exit on error

echo "Installing dependencies..."
pip install -r requirements-production.txt

echo "Creating database schema (if DB_SCHEMA is set)..."
python manage.py create_schema || echo "Schema creation skipped (DB_SCHEMA not set or not PostgreSQL)"

echo "Running database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build complete!"

