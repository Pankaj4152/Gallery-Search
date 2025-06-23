#!/bin/bash

# Gallery Search Startup Script
# This script handles the startup process for Railway/Render deployment

set -e

echo "🚀 Starting Gallery Search..."

# Wait for database to be ready (if using external database)
if [ -n "$DB_HOST" ]; then
    echo "⏳ Waiting for database to be ready..."
    while ! nc -z $DB_HOST ${DB_PORT:-5432}; do
        sleep 1
    done
    echo "✅ Database is ready!"
fi

# Run database migrations
echo "🔄 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Start the application
echo "🎯 Starting Django server..."
exec python manage.py runserver 0.0.0.0:$PORT 