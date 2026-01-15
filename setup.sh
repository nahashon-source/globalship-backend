#!/bin/bash
# GlobalShip Backend Setup Script
# Run this script from your globalship-backend directory

echo "🚀 Setting up GlobalShip Backend..."

# Copy configuration files to root
cat > requirements.txt << 'EOF'
# FastAPI and ASGI server
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
alembic==1.13.1

# Redis
redis==5.0.1
hiredis==2.3.2

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-decouple==3.8
pydantic[email]==2.5.3
pydantic-settings==2.1.0

# Email
python-dotenv==1.0.0
emails==0.6

# CORS
fastapi-cors==0.0.6

# Validation and utilities
email-validator==2.1.0
phonenumbers==8.13.27

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0
faker==22.0.0

# Code quality
black==23.12.1
flake8==7.0.0
mypy==1.8.0
EOF

echo "✅ Created requirements.txt"

# Copy .env.example
cat > .env.example << 'EOF'
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
SECRET_KEY="your-secret-key-here-change-in-production-min-32-characters"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL="postgresql://globalship_user:your_password@localhost:5432/globalship_db"
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# Redis
REDIS_URL="redis://localhost:6379/0"
REDIS_PASSWORD=""
REDIS_MAX_CONNECTIONS=10

# CORS
BACKEND_CORS_ORIGINS='["http://localhost:3000","http://localhost:5173","http://localhost:8080"]'

# Email (Optional - for contact form)
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="your-email@gmail.com"
SMTP_PASSWORD="your-app-password"
EMAILS_FROM_EMAIL="noreply@globalship.com"
EMAILS_FROM_NAME="GlobalShip Logistics"

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# File Upload
MAX_UPLOAD_SIZE=10485760
ALLOWED_EXTENSIONS='["pdf","jpg","jpeg","png","doc","docx"]'

# Logging
LOG_LEVEL="INFO"
EOF

echo "✅ Created .env.example"

# Copy .env from .env.example
cp .env.example .env

echo "✅ Created .env (update with your actual credentials)"

echo ""
echo "📦 Next steps:"
echo "1. Create a Python virtual environment: python3 -m venv venv"
echo "2. Activate it: source venv/bin/activate"
echo "3. Install dependencies: pip install -r requirements.txt"
echo "4. Update .env with your database credentials"
echo ""
echo "✨ Setup complete! Ready for next steps."