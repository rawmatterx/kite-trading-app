# Kite Trading Bot - Backend

This is the backend service for the Kite Trading Bot, built with FastAPI and PostgreSQL.

## Features

- **RESTful API** with FastAPI
- **JWT Authentication**
- **PostgreSQL** database with SQLAlchemy ORM
- **Alembic** for database migrations
- **Kite Connect API** integration
- **Logging** with JSON formatting
- **Environment-based** configuration
- **Docker** support
- **Health checks**
- **Rate limiting**
- **CORS** support
- **Security** best practices

## Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Docker (optional)
- Kite Connect API credentials

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd kite-trading-app/backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   For development, also install:
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Set up environment variables**
   Copy `.env.example` to `.env` and update the values:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your configuration:
   ```env
   # Database
   POSTGRES_SERVER=db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=kiteapp
   POSTGRES_PORT=5432
   
   # Security
   SECRET_KEY=your-secret-key-here
   
   # Kite Connect
   KITE_API_KEY=your-api-key
   KITE_API_SECRET=your-api-secret
   KITE_REDIRECT_URI=http://localhost:3000/auth/callback
   
   # CORS
   CORS_ORIGINS=http://localhost:3000,http://localhost:8000
   
   # Environment
   ENVIRONMENT=development
   DEBUG=True
   LOG_LEVEL=DEBUG
   ```

## Database Setup

1. **Run migrations**
   ```bash
   alembic upgrade head
   ```

   To create a new migration:
   ```bash
   alembic revision --autogenerate -m "Your migration message"
   ```

## Running the Application

### Development

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Production with Docker

1. Build the Docker image:
   ```bash
   docker build -t kite-trading-backend .
   ```

2. Run the container:
   ```bash
   docker run -d --name kite-backend -p 8000:8000 --env-file .env kite-trading-backend
   ```

### Using Docker Compose

```bash
docker-compose up --build
```

## API Documentation

- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`
- **OpenAPI Schema**: `http://localhost:8000/api/openapi.json`

## Testing

```bash
pytest
```

## Linting and Formatting

```bash
# Format code with black and isort
black .
isort .

# Lint with flake8
flake8

# Type checking
mypy .
```

## Deployment

### Production Checklist

- [ ] Set `ENVIRONMENT=production` in `.env`
- [ ] Set `DEBUG=False`
- [ ] Configure a production database
- [ ] Set up proper secrets management
- [ ] Configure HTTPS
- [ ] Set up monitoring and alerting
- [ ] Set up backup and recovery

## License

MIT
