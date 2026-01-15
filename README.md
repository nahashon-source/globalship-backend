# GlobalShip Backend API

A production-ready FastAPI backend for GlobalShip logistics platform with PostgreSQL, Redis, and comprehensive security features.

## Features

- ✅ **FastAPI** - Modern, fast web framework
- ✅ **PostgreSQL** - Robust relational database
- ✅ **Redis** - High-performance caching
- ✅ **SQLAlchemy ORM** - SQL injection protection
- ✅ **JWT Authentication** - Secure token-based auth
- ✅ **Pydantic Validation** - Request/response validation
- ✅ **Alembic Migrations** - Database version control
- ✅ **Docker Support** - Easy deployment
- ✅ **API Documentation** - Auto-generated Swagger/ReDoc

## Quick Start

### 1. Clone and Setup
```bash
# Clone repository
cd globalship-backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

### 3. Setup Database

**Option A: Using Docker (Recommended)**
```bash
# Start PostgreSQL and Redis
docker-compose up -d db redis

# Wait for services to be healthy
docker-compose ps
```

**Option B: Local PostgreSQL**
```bash
# Install PostgreSQL
sudo apt-get install postgresql

# Create database
sudo -u postgres psql
CREATE DATABASE globalship_db;
CREATE USER globalship_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE globalship_db TO globalship_user;
\q
```

### 4. Run Migrations
```bash
# Run Alembic migrations
alembic upgrade head
```

### 5. Start Application

**Development Mode:**
```bash
# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Using Docker:**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api
```

### 6. Access API

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/logout` - Logout user

### Shipments
- `POST /api/v1/shipments/` - Create shipment
- `GET /api/v1/shipments/` - List shipments
- `GET /api/v1/shipments/{id}` - Get shipment
- `PUT /api/v1/shipments/{id}` - Update shipment
- `GET /api/v1/shipments/track/{tracking_number}` - Track shipment

### Quotes
- `POST /api/v1/quotes/` - Request quote
- `GET /api/v1/quotes/` - List quotes
- `GET /api/v1/quotes/{id}` - Get quote

### Dashboard
- `GET /api/v1/dashboard/stats` - Get dashboard statistics

### Contact
- `POST /api/v1/contact/` - Submit contact form

## Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration history
alembic history
```

## Testing
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## Security Features

- ✅ SQL injection protection via SQLAlchemy ORM
- ✅ Password hashing with bcrypt
- ✅ JWT token authentication
- ✅ Input validation with Pydantic
- ✅ CORS configuration
- ✅ Rate limiting ready
- ✅ Sanitized user inputs

## Environment Variables
```env
# Application
PROJECT_NAME="GlobalShip API"
ENVIRONMENT="development"
DEBUG=True

# Database
DATABASE_URL="postgresql://user:password@localhost:5432/globalship_db"

# Redis
REDIS_URL="redis://localhost:6379/0"

# Security
SECRET_KEY="your-secret-key-min-32-characters"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS='["http://localhost:3000"]'
```

## Docker Commands
```bash
# Build and start
docker-compose up --build -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild specific service
docker-compose up -d --build api

# Access database
docker-compose exec db psql -U globalship_user -d globalship_db

# Access Redis CLI
docker-compose exec redis redis-cli
```

## Production Deployment

1. **Update environment variables**
   - Set `ENVIRONMENT=production`
   - Set `DEBUG=False`
   - Use strong `SECRET_KEY`
   - Configure production database

2. **Use production server**
```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

3. **Enable HTTPS**
   - Use reverse proxy (Nginx/Traefik)
   - Configure SSL certificates

4. **Setup monitoring**
   - Application logs
   - Database monitoring
   - Redis monitoring

## Beekeeper Studio Connection

**PostgreSQL Connection:**
- Host: `localhost`
- Port: `5432`
- Database: `globalship_db`
- Username: `globalship_user`
- Password: `globalship_password`

## Project Structure
```
globalship-backend/
├── app/
│   ├── api/           # API routes
│   ├── core/          # Core configuration
│   ├── db/            # Database setup
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic
│   └── main.py        # Application entry
├── alembic/           # Database migrations
├── tests/             # Test suite
├── .env               # Environment variables
├── docker-compose.yml # Docker setup
└── requirements.txt   # Dependencies
```

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
# globalship-backend
