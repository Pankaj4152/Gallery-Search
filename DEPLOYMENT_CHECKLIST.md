# 🚀 Deployment Checklist

## ✅ Pre-Deployment Checklist

### 1. Files Ready
- [ ] `Dockerfile` exists (not `Dockerfile.prod`)
- [ ] `railway.toml` configured
- [ ] `render.yaml` configured (if using Render)
- [ ] `requirements.txt` updated with production dependencies
- [ ] `.dockerignore` created
- [ ] `start.sh` created and executable

### 2. Environment Variables
- [ ] `DJANGO_SETTINGS_MODULE=GallerySearch.settings_prod`
- [ ] `SECRET_KEY` (generate a secure one)
- [ ] `ALLOWED_HOSTS` (platform-specific domains)
- [ ] `CELERY_BROKER_URL` (Redis connection string)
- [ ] Database credentials (if using external DB)

### 3. Code Changes
- [ ] Health check endpoint added (`/`)
- [ ] Production settings configured
- [ ] Static files configuration updated
- [ ] CORS settings updated
- [ ] Logging configured

### 4. Dependencies
- [ ] `gunicorn` added to requirements.txt
- [ ] `whitenoise` added to requirements.txt
- [ ] `psycopg2-binary` added to requirements.txt
- [ ] `django-redis` added to requirements.txt

## 🚀 Railway Deployment Steps

### 1. Push to GitHub
```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### 2. Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect your `docker-compose.yml`

### 3. Configure Environment Variables
In Railway dashboard, add:
```bash
DJANGO_SETTINGS_MODULE=GallerySearch.settings_prod
SECRET_KEY=your-secure-secret-key-here
ALLOWED_HOSTS=.railway.app
CELERY_BROKER_URL=redis://redis:6379/0
```

### 4. Monitor Deployment
- Check build logs for any errors
- Verify health check endpoint responds
- Test API endpoints

## 🔧 Troubleshooting

### Common Issues:

1. **"Dockerfile does not exist"**
   - ✅ Ensure `Dockerfile` (not `Dockerfile.prod`) exists in root
   - ✅ Check file permissions

2. **Build fails**
   - ✅ Check `requirements.txt` for syntax errors
   - ✅ Verify all dependencies are available
   - ✅ Check `.dockerignore` isn't excluding needed files

3. **Database connection fails**
   - ✅ Verify database credentials
   - ✅ Check if database service is running
   - ✅ Test connection manually

4. **Static files not loading**
   - ✅ Check `STATIC_ROOT` setting
   - ✅ Verify `whitenoise` is configured
   - ✅ Run `collectstatic` manually if needed

5. **Celery worker not starting**
   - ✅ Check Redis connection
   - ✅ Verify `CELERY_BROKER_URL`
   - ✅ Check worker logs

### Quick Fixes:

```bash
# Generate secure secret key
python -c "import secrets; print(secrets.token_hex(50))"

# Test database connection
python manage.py dbshell

# Test Redis connection
redis-cli ping

# Check static files
python manage.py collectstatic --dry-run

# Test health check
curl https://your-app.railway.app/
```

## 📊 Deployment Status

| Component | Status | Notes |
|-----------|--------|-------|
| Dockerfile | ✅ Ready | Production optimized |
| Railway Config | ✅ Ready | Auto-detects docker-compose.yml |
| Environment Vars | ⚠️ Needs Setup | Configure in Railway dashboard |
| Database | ✅ Ready | Uses Railway PostgreSQL |
| Redis | ✅ Ready | Uses Railway Redis |
| Health Check | ✅ Ready | Endpoint at `/` |
| Static Files | ✅ Ready | Whitenoise configured |
| Celery Workers | ✅ Ready | Background processing |

## 🎯 Next Steps After Deployment

1. **Test the application**
   - Visit your Railway URL
   - Test image upload
   - Test search functionality
   - Check Celery worker logs

2. **Configure custom domain** (optional)
   - Add custom domain in Railway
   - Update DNS settings
   - Configure SSL certificate

3. **Set up monitoring**
   - Enable Railway monitoring
   - Set up error tracking
   - Configure alerts

4. **Deploy frontend**
   - Deploy React app to Vercel/Netlify
   - Update API endpoints
   - Test full integration

## 🆘 Need Help?

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Django Deployment**: [docs.djangoproject.com/en/stable/howto/deployment](https://docs.djangoproject.com/en/stable/howto/deployment)
- **Docker Docs**: [docs.docker.com](https://docs.docker.com)

**Your deployment should work now! 🚀** 