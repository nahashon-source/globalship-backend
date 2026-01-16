#!/bin/bash

echo "🔧 Fixing GlobalShip Backend Setup..."

# Fix .env file
echo "1️⃣ Fixing .env file..."
cat > .env << 'ENVEOF'
PROJECT_NAME="GlobalShip API"
VERSION="1.0.0"
API_V1_PREFIX="/api/v1"
ENVIRONMENT="development"
DEBUG=True
HOST=0.0.0.0
PORT=8000
SECRET_KEY="your-secret-key-here-change-in-production-min-32-characters-long"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
DATABASE_URL="postgresql://globalship_user:globalship_password@localhost:5432/globalship_db"
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
REDIS_URL="redis://localhost:6379/0"
REDIS_PASSWORD=""
REDIS_MAX_CONNECTIONS=10
BACKEND_CORS_ORIGINS='["http://localhost:3000","http://localhost:5173","http://localhost:8080"]'
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="your-email@gmail.com"
SMTP_PASSWORD="your-app-password"
EMAILS_FROM_EMAIL="noreply@globalship.com"
EMAILS_FROM_NAME="GlobalShip Logistics"
RATE_LIMIT_PER_MINUTE=60
MAX_UPLOAD_SIZE=10485760
ALLOWED_EXTENSIONS='["pdf","jpg","jpeg","png","doc","docx"]'
LOG_LEVEL="INFO"
ENVEOF

# Install missing dependencies
echo "2️⃣ Installing pydantic-settings..."
pip install pydantic-settings==2.1.0

# Create scripts directory
echo "3️⃣ Creating scripts directory..."
mkdir -p scripts

# Restart Docker services
echo "4️⃣ Restarting Docker services..."
docker-compose down
docker-compose up -d db redis

# Wait for services
echo "5️⃣ Waiting for services to be ready..."
sleep 15

# Run migrations
echo "6️⃣ Running database migrations..."
alembic upgrade head

# Create test database
echo "7️⃣ Creating test database..."
docker-compose exec -T db psql -U globalship_user -c "CREATE DATABASE test_db;" 2>/dev/null || echo "Test DB may already exist"

echo ""
echo "✅ Setup fixed! Now run:"
echo "   uvicorn app.main:app --reload"
echo ""
echo "Then in another terminal:"
echo "   python test_api.py"
