# GlobalShip Backend API - Production Ready

A comprehensive, production-ready FastAPI backend for GlobalShip logistics platform with PostgreSQL, Redis, JWT authentication, and complete CRUD operations for shipment management.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![Redis](https://img.shields.io/badge/Redis-7-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [Available Endpoints](#available-endpoints)
- [Security Features](#security-features)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)

## 🎯 Overview

GlobalShip Backend is a comprehensive RESTful API designed for logistics and freight management. It provides complete shipment tracking, quote management, user authentication, and administrative capabilities.

**Key Capabilities:**
- User registration and JWT-based authentication
- Shipment creation, tracking, and management
- Real-time shipment event timeline
- Quote request and management system
- Contact form handling
- Admin dashboard with system statistics
- Role-based access control (RBAC)
- Rate limiting and security features

## ✨ Features

### Core Features
- ✅ **User Management**
  - Registration with email validation
  - JWT token-based authentication
  - Password hashing with bcrypt
  - Role-based access (admin/user)
  - User profile management

- ✅ **Shipment Management**
  - Create and track shipments
  - Unique tracking number generation
  - Multiple service types (Air, Sea, Road, Warehousing)
  - Real-time status updates
  - Shipment event timeline
  - Public tracking endpoint (no auth required)

- ✅ **Quote System**
  - Request quotes for shipments
  - Admin quote approval workflow
  - Quote expiration handling
  - Price estimation

- ✅ **Contact & Communication**
  - Contact form submissions
  - Email notification system
  - Admin message management

- ✅ **Dashboard & Analytics**
  - User dashboard with statistics
  - Admin system overview
  - Revenue tracking
  - Active shipment monitoring

### Security Features
- 🔒 SQL injection protection via SQLAlchemy ORM
- 🔒 Password hashing with bcrypt
- 🔒 JWT token authentication
- 🔒 Input validation with Pydantic schemas
- 🔒 CORS configuration
- 🔒 Rate limiting (60 requests/minute)
- 🔒 XSS protection through input sanitization
- 🔒 Secure password requirements

### Production Features
- 📊 Comprehensive logging system
- 📊 Redis caching for performance
- 📊 Database connection pooling
- 📊 Health check endpoints
- 📊 Error handling and custom exceptions
- 📊 Request validation
- 📊 API documentation (Swagger/ReDoc)

## 🛠 Technology Stack

### Core Technologies
- **FastAPI 0.109.0** - Modern, fast web framework
- **Python 3.8+** - Programming language
- **PostgreSQL 15** - Relational database
- **Redis 7** - Caching and session management
- **SQLAlchemy 2.0** - ORM for database operations
- **Alembic 1.13** - Database migrations
- **Pydantic 1.10** - Data validation

### Authentication & Security
- **python-jose** - JWT token handling
- **passlib + bcrypt** - Password hashing
- **email-validator** - Email validation

### Development Tools
- **Uvicorn** - ASGI server
- **pytest** - Testing framework
- **Black** - Code formatting
- **Flake8** - Linting

## 📁 Project Structure
```
globalship-backend/
├── app/
│   ├── api/
│   │   ├── dependencies.py          # Auth dependencies
│   │   └── v1/
│   │       ├── api.py               # Main API router
│   │       └── endpoints/
│   │           ├── auth.py          # Authentication
│   │           ├── users.py         # User management
│   │           ├── shipments.py     # Shipment CRUD
│   │           ├── shipment_events.py # Event timeline
│   │           ├── quotes.py        # Quote management
│   │           ├── contact.py       # Contact form
│   │           ├── dashboard.py     # Dashboard stats
│   │           └── admin.py         # Admin endpoints
│   ├── core/
│   │   ├── config.py                # Application settings
│   │   └── security.py              # Security utilities
│   ├── db/
│   │   ├── base.py                  # SQLAlchemy base
│   │   └── session.py               # DB session management
│   ├── models/                      # SQLAlchemy models
│   │   ├── user.py
│   │   ├── shipment.py
│   │   ├── shipment_event.py
│   │   ├── quote.py
│   │   └── contact_message.py
│   ├── schemas/                     # Pydantic schemas
│   │   ├── user.py
│   │   ├── shipment.py
│   │   ├── shipment_event.py
│   │   ├── quote.py
│   │   ├── contact_message.py
│   │   └── dashboard.py
│   ├── services/                    # Business logic
│   │   ├── redis_service.py
│   │   ├── user_service.py
│   │   ├── shipment_service.py
│   │   ├── shipment_event_service.py
│   │   ├── quote_service.py
│   │   ├── contact_message_service.py
│   │   └── email_service.py
│   ├── middleware/
│   │   └── rate_limit.py            # Rate limiting
│   ├── utils/
│   │   ├── logger.py                # Logging setup
│   │   ├── exceptions.py            # Custom exceptions
│   │   └── error_handlers.py        # Error handling
│   └── main.py                      # Application entry
├── alembic/                         # Database migrations
│   └── versions/
├── scripts/
│   └── seed_data.py                 # Seed database
├── tests/                           # Test suite
├── logs/                            # Application logs
├── .env                             # Environment variables
├── .env.example                     # Environment template
├── requirements.txt                 # Python dependencies
├── alembic.ini                      # Alembic config
└── README.md                        # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 15
- Redis 7
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/globalship-backend.git
cd globalship-backend
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
# Application
PROJECT_NAME="GlobalShip API"
VERSION="1.0.0"
API_V1_PREFIX="/api/v1"
ENVIRONMENT="development"
DEBUG=True

# Server
HOST=0.0.0.0
PORT=8000

# Security
SECRET_KEY="your-secret-key-min-32-characters-change-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL="postgresql://globalship_user:globalship_password@localhost:5432/globalship_db"
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# Redis
REDIS_URL="redis://localhost:6379/0"
REDIS_PASSWORD=""
REDIS_MAX_CONNECTIONS=10

# CORS (Add your frontend URLs)
BACKEND_CORS_ORIGINS='["http://localhost:3000","http://localhost:5173","http://localhost:8080"]'

# Email (Optional - for notifications)
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="your-email@gmail.com"
SMTP_PASSWORD="your-app-password"
EMAILS_FROM_EMAIL="noreply@globalship.com"
EMAILS_FROM_NAME="GlobalShip Logistics"

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# Logging
LOG_LEVEL="INFO"
```

## 💾 Database Setup

### Option 1: Local PostgreSQL
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql

# Create database and user
sudo -u postgres psql << 'SQL'
CREATE USER globalship_user WITH PASSWORD 'globalship_password';
CREATE DATABASE globalship_db OWNER globalship_user;
GRANT ALL PRIVILEGES ON DATABASE globalship_db TO globalship_user;
\q
SQL
```

### Option 2: Using Docker
```bash
docker-compose up -d db redis
```

### Run Database Migrations
```bash
# Run Alembic migrations
alembic upgrade head
```

### Verify Database
```bash
# List all tables
psql -U globalship_user -d globalship_db -h localhost -c "\dt"

# Expected tables:
# - users
# - shipments
# - shipment_events
# - quotes
# - contact_messages
```

## 🏃 Running the Application

### Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Python
```bash
python -m app.main
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc
- **Health Check**: http://localhost:8000/health

## 📚 API Documentation

### Interactive Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc

### Quick Start Guide

1. **Register a User**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "full_name": "John Doe",
    "company_name": "Acme Corp"
  }'
```

2. **Login**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

3. **Create Shipment** (Use the access token)
```bash
curl -X POST http://localhost:8000/api/v1/shipments/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "origin_city": "Nairobi",
    "origin_country": "Kenya",
    "destination_city": "Dar es Salaam",
    "destination_country": "Tanzania",
    "service_type": "air",
    "weight": 25.5,
    "package_count": 2
  }'
```

4. **Track Shipment** (Public - no auth required)
```bash
curl http://localhost:8000/api/v1/shipments/track/GS123ABC456
```

## 🔐 Authentication

### JWT Token Authentication

The API uses JWT (JSON Web Tokens) for authentication.

**Token Flow:**
1. User registers or logs in
2. Server returns `access_token` and `refresh_token`
3. Client includes token in `Authorization` header: `Bearer <token>`
4. Server validates token on protected endpoints

**Token Expiration:**
- Access Token: 30 minutes
- Refresh Token: 7 days

### Protected Endpoints

Include the JWT token in the Authorization header:
```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### User Roles

- **Regular User**: Can manage their own shipments and quotes
- **Admin** (`is_superuser=true`): Full system access, can view all data

## 📡 Available Endpoints

### Authentication (`/api/v1/auth`)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register` | Register new user | No |
| POST | `/login` | Login user | No |
| GET | `/me` | Get current user | Yes |
| POST | `/logout` | Logout user | Yes |

### Users (`/api/v1/users`)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/me` | Get current user | Yes |
| PUT | `/me` | Update current user | Yes |
| GET | `/` | Get all users (admin) | Admin |

### Shipments (`/api/v1/shipments`)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/` | Create shipment | Yes |
| GET | `/` | List user's shipments | Yes |
| GET | `/{id}` | Get shipment by ID | Yes |
| PUT | `/{id}` | Update shipment | Yes |
| GET | `/track/{tracking_number}` | Track shipment (public) | No |

### Shipment Events (`/api/v1/events`)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/` | Create shipment event | Yes |
| GET | `/{shipment_id}/timeline` | Get shipment timeline | Yes |
| GET | `/track/{tracking_number}/timeline` | Public timeline | No |

### Quotes (`/api/v1/quotes`)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/` | Request quote | Yes |
| GET | `/` | List user's quotes | Yes |
| GET | `/{id}` | Get quote by ID | Yes |
| PUT | `/{id}` | Update quote | Yes |

### Dashboard (`/api/v1/dashboard`)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/stats` | Get dashboard statistics | Yes |

### Contact (`/api/v1/contact`)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/` | Submit contact form | No |

### Admin (`/api/v1/admin`)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/stats` | System statistics | Admin |
| GET | `/users` | List all users | Admin |
| GET | `/shipments` | List all shipments | Admin |
| PUT | `/shipments/{id}/status` | Update shipment | Admin |
| GET | `/quotes` | List all quotes | Admin |
| PUT | `/quotes/{id}` | Update quote | Admin |
| GET | `/messages` | List contact messages | Admin |

### Health Check
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | API info | No |
| GET | `/health` | Detailed health check | No |

## 🔒 Security Features

### Implemented Security Measures

1. **SQL Injection Protection**
   - All queries use SQLAlchemy ORM
   - Parameterized queries throughout
   - No raw SQL execution with user input

2. **Authentication Security**
   - JWT tokens with expiration
   - Password hashing with bcrypt
   - Secure password requirements (min 6 chars, letters + numbers)

3. **Input Validation**
   - Pydantic schemas validate all inputs
   - XSS protection through sanitization
   - Email validation
   - Phone number validation

4. **Rate Limiting**
   - 60 requests per minute per IP
   - Redis-based tracking
   - Automatic expiration

5. **CORS Configuration**
   - Configurable allowed origins
   - Credentials support
   - Method and header restrictions

6. **Error Handling**
   - Custom exception handlers
   - Sanitized error messages
   - Detailed logging

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py -v
```

### Test User Creation

Create test users via API:
```bash
# Register test user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123456",
    "full_name": "Test User"
  }'
```

Or use the seed script:
```bash
python scripts/seed_data.py
```

This creates:
- Admin: `admin@globalship.com` / `Admin123456`
- Demo: `demo@globalship.com` / `Demo123456`

## 🌐 Deployment

### Production Checklist

- [ ] Update `SECRET_KEY` in `.env`
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=False`
- [ ] Configure production database
- [ ] Setup Redis in production
- [ ] Configure CORS for production frontend
- [ ] Setup HTTPS/SSL certificates
- [ ] Configure email service (SMTP)
- [ ] Setup logging and monitoring
- [ ] Configure backup strategy
- [ ] Setup CI/CD pipeline

### Deploy with Gunicorn
```bash
gunicorn app.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --log-level info \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log
```

### Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name api.globalship.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 🗄️ Database Schema

### Users Table
```sql
- id (UUID, PK)
- email (VARCHAR, UNIQUE)
- hashed_password (VARCHAR)
- company_name (VARCHAR, NULL)
- phone (VARCHAR, NULL)
- full_name (VARCHAR, NULL)
- is_active (BOOLEAN, DEFAULT TRUE)
- is_verified (BOOLEAN, DEFAULT FALSE)
- is_superuser (BOOLEAN, DEFAULT FALSE)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- last_login (TIMESTAMP, NULL)
```

### Shipments Table
```sql
- id (UUID, PK)
- tracking_number (VARCHAR, UNIQUE)
- user_id (UUID, FK → users)
- origin_city, origin_country
- destination_city, destination_country
- service_type (ENUM)
- status (ENUM)
- weight, dimensions, package_count
- estimated_cost, actual_cost, currency
- created_at, updated_at
- estimated_delivery, actual_delivery
```

### Other Tables
- **shipment_events**: Event timeline for shipments
- **quotes**: Quote requests and responses
- **contact_messages**: Contact form submissions

## 🔄 Connecting Frontend

### Backend URL Configuration

Your backend is available at:
```
http://localhost:8000
```

### Frontend Environment Variables

In your React frontend, create `.env`:
```env
VITE_API_URL=http://localhost:8000/api/v1
```

### Example Frontend API Service
```javascript
// src/services/api.js
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getCurrentUser: () => api.get('/auth/me'),
};

export const shipmentAPI = {
  create: (data) => api.post('/shipments/', data),
  list: (params) => api.get('/shipments/', { params }),
  track: (trackingNumber) => api.get(`/shipments/track/${trackingNumber}`),
};

export const dashboardAPI = {
  getStats: () => api.get('/dashboard/stats'),
};

export default api;
```

## 📊 Monitoring & Logging

### Application Logs

Logs are stored in the `logs/` directory:
- `logs/app.log` - All application logs
- `logs/error.log` - Error logs only

### View Logs
```bash
# View all logs
tail -f logs/app.log

# View errors only
tail -f logs/error.log
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- **Brian Munene** - *Initial work*

## 🙏 Acknowledgments

- FastAPI documentation
- SQLAlchemy team
- The Python community

## 📧 Support

For support, email support@globalship.com or open an issue on GitHub.

---

**Built with ❤️ using FastAPI**
