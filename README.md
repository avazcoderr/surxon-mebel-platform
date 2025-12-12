# Railway Django Deployment Configuration

This project is configured for deployment on Railway using Docker.

## Files Added/Modified for Railway:

1. **Dockerfile** - Optimized for Railway deployment
2. **docker-compose.yml** - For local development
3. **Procfile** - Railway process definition
4. **railway.sh** - Railway deployment script
5. **entrypoint.sh** - Container entrypoint script
6. **config/settings.py** - Updated with environment variables

## Environment Variables for Railway:

Set these in your Railway project:
- `SECRET_KEY` - Django secret key for production
- `DEBUG` - Set to 'False' for production
- `PORT` - Automatically set by Railway

## Deployment Steps:

1. Connect your repository to Railway
2. Railway will automatically detect the Dockerfile
3. Set environment variables in Railway dashboard
4. Deploy!

## Local Development:

```bash
docker-compose up --build
```

## Manual Docker Build:

```bash
docker build -t surxon-mebel .
docker run -p 8000:8000 surxon-mebel
```