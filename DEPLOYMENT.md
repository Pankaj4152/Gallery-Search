# 🚀 Gallery Search Deployment Guide

This guide covers deployment options for your AI-powered image search application.

## 📋 Prerequisites

Before deploying, ensure you have:
- [ ] Git repository with your code
- [ ] All dependencies installed locally
- [ ] Environment variables configured
- [ ] Database migrations ready

## 🥇 Recommended: Railway Deployment

### Why Railway?
- ✅ **Easiest deployment** - One-click from GitHub
- ✅ **Built-in Redis** support
- ✅ **Automatic scaling** for Celery workers
- ✅ **Free tier** available
- ✅ **Docker support** (works with your docker-compose.yml)

### Step-by-Step Railway Deployment:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Railway deployment"
   git push origin main
   ```

2. **Deploy to Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect your `docker-compose.yml`

3. **Configure Environment Variables**
   ```bash
   # In Railway dashboard, add these variables:
   DJANGO_SETTINGS_MODULE=GallerySearch.settings_prod
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=.railway.app
   CELERY_BROKER_URL=redis://redis:6379/0
   ```

4. **Deploy**
   - Railway will automatically build and deploy
   - Your app will be available at `https://your-app.railway.app`

**Cost:** Free tier → $5-20/month for production

---

## 🥈 Alternative: Render Deployment

### Why Render?
- ✅ **Free tier** for web services
- ✅ **Redis add-on** available
- ✅ **Background workers** support
- ✅ **Auto-deploy** from GitHub

### Step-by-Step Render Deployment:

1. **Prepare your repository**
   - Ensure `render.yaml` is in your root directory
   - Push to GitHub

2. **Deploy to Render**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Click "New +" → "Blueprint"
   - Connect your repository
   - Render will auto-detect `render.yaml`

3. **Monitor Deployment**
   - Render will create all services automatically
   - Check logs for any issues

**Cost:** Free tier → $7-25/month for production

---

## 🥉 Traditional: Heroku Deployment

### Why Heroku?
- ✅ **Mature platform** with good documentation
- ✅ **Add-ons ecosystem**
- ⚠️ **No free tier** anymore
- ⚠️ **More expensive** than alternatives

### Step-by-Step Heroku Deployment:

1. **Install Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create your-gallery-search-app
   ```

3. **Add Add-ons**
   ```bash
   heroku addons:create heroku-redis:hobby-dev
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Configure Environment**
   ```bash
   heroku config:set DJANGO_SETTINGS_MODULE=GallerySearch.settings_prod
   heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(50))')
   ```

5. **Deploy**
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   ```

**Cost:** $25-100/month

---

## 🏢 Enterprise: AWS/GCP/Azure

### AWS ECS Deployment:

1. **Create ECR Repository**
   ```bash
   aws ecr create-repository --repository-name gallery-search
   ```

2. **Build and Push Docker Image**
   ```bash
   docker build -t gallery-search .
   aws ecr get-login-password | docker login --username AWS --password-stdin your-account.dkr.ecr.region.amazonaws.com
   docker tag gallery-search:latest your-account.dkr.ecr.region.amazonaws.com/gallery-search:latest
   docker push your-account.dkr.ecr.region.amazonaws.com/gallery-search:latest
   ```

3. **Create ECS Cluster and Services**
   - Use AWS Console or CloudFormation
   - Configure Fargate tasks for Django and Celery
   - Set up RDS PostgreSQL and ElastiCache Redis

**Cost:** $20-100/month

### Google Cloud Run:

1. **Enable APIs**
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

2. **Deploy**
   ```bash
   gcloud run deploy gallery-search-backend \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

**Cost:** $25-120/month

---

## 🔧 Production Configuration

### Environment Variables:
```bash
# Required
DJANGO_SETTINGS_MODULE=GallerySearch.settings_prod
SECRET_KEY=your-secure-secret-key
ALLOWED_HOSTS=your-domain.com

# Database
DB_NAME=gallery_search
DB_USER=postgres
DB_PASSWORD=secure-password
DB_HOST=your-db-host
DB_PORT=5432

# Celery
CELERY_BROKER_URL=redis://your-redis-host:6379/0

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Security Checklist:
- [ ] `DEBUG=False` in production
- [ ] Secure `SECRET_KEY`
- [ ] HTTPS enabled
- [ ] CORS properly configured
- [ ] Database credentials secured
- [ ] Static files served via CDN

---

## 🎨 Frontend Deployment

### Vercel (Recommended):
1. Connect GitHub repository
2. Set build command: `cd frontend && npm install && npm run build`
3. Set output directory: `frontend/dist`
4. Configure environment variables for API endpoints

### Netlify:
1. Connect GitHub repository
2. Set build command: `cd frontend && npm install && npm run build`
3. Set publish directory: `frontend/dist`

### AWS S3 + CloudFront:
1. Build frontend: `cd frontend && npm run build`
2. Upload to S3 bucket
3. Configure CloudFront distribution
4. Set up custom domain

---

## 🚨 Troubleshooting

### Common Issues:

1. **Celery Worker Not Starting**
   ```bash
   # Check Redis connection
   redis-cli ping
   
   # Check Celery logs
   celery -A GallerySearch worker --loglevel=debug
   ```

2. **Database Connection Issues**
   ```bash
   # Test database connection
   python manage.py dbshell
   
   # Run migrations
   python manage.py migrate
   ```

3. **Static Files Not Loading**
   ```bash
   # Collect static files
   python manage.py collectstatic --noinput
   
   # Check STATIC_ROOT setting
   ```

4. **ML Models Not Loading**
   ```bash
   # Check model cache directory
   ls ~/.cache/huggingface/
   
   # Increase memory limits if needed
   ```

### Performance Optimization:

1. **Database**
   - Use connection pooling
   - Add database indexes
   - Optimize queries

2. **Caching**
   - Redis for session storage
   - CDN for static files
   - Cache ML model results

3. **Monitoring**
   - Set up logging
   - Monitor resource usage
   - Set up alerts

---

## 📊 Cost Comparison

| Platform | Free Tier | Production Cost | Ease of Use | Features |
|----------|-----------|-----------------|-------------|----------|
| **Railway** | ✅ | $5-20/month | ⭐⭐⭐⭐⭐ | Full stack, Redis, Workers |
| **Render** | ✅ | $7-25/month | ⭐⭐⭐⭐ | Good free tier, Workers |
| **Heroku** | ❌ | $25-100/month | ⭐⭐⭐ | Mature, Add-ons |
| **AWS** | ✅ | $20-100/month | ⭐⭐ | Scalable, Complex |
| **GCP** | ✅ | $25-120/month | ⭐⭐ | ML integration |
| **Azure** | ✅ | $30-150/month | ⭐⭐ | Enterprise features |

---

## 🎯 Quick Start Commands

```bash
# Railway (Recommended)
npm install -g @railway/cli
railway login
railway up

# Render
# Just push to GitHub and connect to Render

# Heroku
heroku create
heroku addons:create heroku-redis:hobby-dev
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main

# Use our deployment script
chmod +x deploy.sh
./deploy.sh
```

---

## 🆘 Need Help?

- **Railway**: [docs.railway.app](https://docs.railway.app)
- **Render**: [render.com/docs](https://render.com/docs)
- **Heroku**: [devcenter.heroku.com](https://devcenter.heroku.com)
- **AWS**: [aws.amazon.com/documentation](https://aws.amazon.com/documentation)

**Recommendation:** Start with **Railway** for the easiest deployment experience! 