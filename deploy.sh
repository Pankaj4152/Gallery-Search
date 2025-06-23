#!/bin/bash

# Gallery Search Deployment Script
# This script helps deploy to various platforms

set -e

echo "🚀 Gallery Search Deployment Script"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the project root."
    exit 1
fi

# Function to deploy to Railway
deploy_railway() {
    echo "📦 Deploying to Railway..."
    
    # Check if Railway CLI is installed
    if ! command -v railway &> /dev/null; then
        echo "📥 Installing Railway CLI..."
        npm install -g @railway/cli
    fi
    
    # Login to Railway
    railway login
    
    # Deploy
    railway up
    
    echo "✅ Railway deployment initiated!"
}

# Function to deploy to Render
deploy_render() {
    echo "📦 Deploying to Render..."
    
    # Check if render.yaml exists
    if [ ! -f "render.yaml" ]; then
        echo "❌ render.yaml not found. Please create it first."
        exit 1
    fi
    
    echo "📋 Please follow these steps:"
    echo "1. Go to https://render.com"
    echo "2. Connect your GitHub repository"
    echo "3. Create a new Web Service"
    echo "4. Select your repository"
    echo "5. Render will auto-detect render.yaml"
    echo "6. Deploy!"
}

# Function to deploy to Heroku
deploy_heroku() {
    echo "📦 Deploying to Heroku..."
    
    # Check if Heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        echo "📥 Installing Heroku CLI..."
        curl https://cli-assets.heroku.com/install.sh | sh
    fi
    
    # Login to Heroku
    heroku login
    
    # Create app if it doesn't exist
    if [ -z "$HEROKU_APP_NAME" ]; then
        echo "📝 Creating Heroku app..."
        heroku create
    else
        heroku git:remote -a $HEROKU_APP_NAME
    fi
    
    # Add Redis addon
    heroku addons:create heroku-redis:hobby-dev
    
    # Add PostgreSQL addon
    heroku addons:create heroku-postgresql:hobby-dev
    
    # Set environment variables
    heroku config:set DJANGO_SETTINGS_MODULE=GallerySearch.settings_prod
    heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(50))')
    
    # Deploy
    git push heroku main
    
    # Run migrations
    heroku run python manage.py migrate
    
    echo "✅ Heroku deployment complete!"
}

# Function to deploy to DigitalOcean
deploy_digitalocean() {
    echo "📦 Deploying to DigitalOcean App Platform..."
    
    echo "📋 Please follow these steps:"
    echo "1. Go to https://cloud.digitalocean.com/apps"
    echo "2. Create a new app"
    echo "3. Connect your GitHub repository"
    echo "4. Configure services:"
    echo "   - Web service (Django)"
    echo "   - Worker service (Celery)"
    echo "   - Redis database"
    echo "5. Deploy!"
}

# Main menu
echo "Choose your deployment platform:"
echo "1) Railway (Recommended - Easiest)"
echo "2) Render (Good alternative)"
echo "3) Heroku (Traditional)"
echo "4) DigitalOcean App Platform"
echo "5) Exit"

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        deploy_railway
        ;;
    2)
        deploy_render
        ;;
    3)
        deploy_heroku
        ;;
    4)
        deploy_digitalocean
        ;;
    5)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac 