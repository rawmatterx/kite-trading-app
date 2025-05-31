# Deployment Guide

This guide explains how to deploy the Kite Trading App to Render or Railway.

## Prerequisites

- Git
- Docker (for local testing)
- Render or Railway account
- Kite Connect API credentials

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# Project
PROJECT_NAME="Kite Trading App"
VERSION=1.0.0
ENVIRONMENT=production
DEBUG=false

# Server
HOST=0.0.0.0
PORT=8000
WORKERS=4
LOG_LEVEL=info

# Kite Connect
KITE_API_KEY=your_api_key
KITE_API_SECRET=your_api_secret
KITE_REDIRECT_URI=your_redirect_uri

# Security
SECRET_KEY=generate_a_secure_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours

# Database (for local development)
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=kiteapp
DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_SERVER}:${POSTGRES_PORT}/${POSTGRES_DB}
```

## Deployment to Render

1. Push your code to a GitHub repository
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New" and select "Blueprint from Git"
4. Connect your GitHub repository
5. Select the repository and branch
6. Set the following configuration:
   - Name: `kite-backend`
   - Region: Select the one closest to you
   - Branch: `main` or your preferred branch
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables: Copy from your `.env` file

## Deployment to Railway

1. Install Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```

2. Login to Railway:
   ```bash
   railway login
   ```

3. Link your project:
   ```bash
   railway init
   ```

4. Deploy:
   ```bash
   railway up
   ```

5. Set environment variables:
   ```bash
   railway variables set NODE_ENV production
   railway variables set KITE_API_KEY your_api_key
   railway variables set KITE_API_SECRET your_api_secret
   railway variables set SECRET_KEY $(openssl rand -hex 32)
   ```

## Database Setup

For production, you'll need to set up a PostgreSQL database. Both Render and Railway offer managed PostgreSQL databases.

### On Render:
1. Go to Dashboard > New > PostgreSQL
2. Configure the database
3. Get the connection string and add it to your environment variables as `DATABASE_URL`

### On Railway:
1. Run: `railway add --plugin postgresql`
2. The `DATABASE_URL` will be automatically set

## Frontend Deployment

1. Build the frontend:
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. Deploy the `dist` folder to a static hosting service like Vercel, Netlify, or Render's static site hosting.

## Health Check

The application exposes a health check endpoint at `/api/v1/health` that can be used for monitoring.

## Monitoring

- Set up logging and monitoring using the platform's built-in tools
- Configure alerts for errors and performance issues
- Monitor API rate limits for Kite Connect

## Security Considerations

- Never commit `.env` files
- Use HTTPS for all API requests
- Set appropriate CORS policies
- Regularly rotate API keys and secrets
- Monitor for suspicious activity

## Troubleshooting

- Check logs using `railway logs` or in the Render dashboard
- Verify environment variables are set correctly
- Ensure the database is accessible from your application
- Check Kite Connect API status at https://kite.trade/status/
