#!/bin/bash

echo "🚀 Setting up ReelRanker Database..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Navigate to deployment directory
cd deployment

# Start PostgreSQL and Redis
echo "📦 Starting PostgreSQL and Redis containers..."
docker-compose up -d

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 10

# Test database connection
echo "🔍 Testing database connection..."
docker exec reelranker-postgres psql -U reelranker -d reelranker -c "SELECT version();"

if [ $? -eq 0 ]; then
    echo "✅ Database setup completed successfully!"
    echo "📊 PostgreSQL: localhost:5432"
    echo "🔴 Redis: localhost:6379"
    echo ""
    echo "🔧 Next steps:"
    echo "1. Update your .env file with the database credentials"
    echo "2. Run database migrations: python -m alembic upgrade head"
    echo "3. Start the API server: python -m uvicorn app.main:app --reload"
else
    echo "❌ Database setup failed!"
    exit 1
fi
