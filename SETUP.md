# ReelRanker Setup Guide

## Prerequisites

- Python 3.8+
- Docker Desktop
- Git

## Quick Setup

### 1. Clone and Setup Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup Database

```bash
# Start Docker Desktop first, then run:
../scripts/setup_db.sh
```

This will:
- Start PostgreSQL on port 5432
- Start Redis on port 6379
- Create the database and user

### 3. Run Database Migrations

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 4. Start the Server

```bash
# Start the FastAPI server
python -m uvicorn app.main:app --reload
```

The API will be available at: http://localhost:8000

## Database Configuration

### PostgreSQL
- **Host**: localhost
- **Port**: 5432
- **Database**: reelranker
- **Username**: reelranker
- **Password**: reelranker123

### Redis
- **Host**: localhost
- **Port**: 6379

## API Endpoints

- **Health Check**: `GET /health`
- **API Docs**: `GET /docs`
- **Trending Shorts**: `GET /api/v1/shorts/trending`
- **Topic Analysis**: `POST /api/v1/shorts/analyze`
- **Generate Content**: `POST /api/v1/generate`
- **Viral Score**: `POST /api/v1/score`

## Environment Variables

Create a `.env` file in the backend directory:

```env
# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=ReelRanker API
VERSION=1.0.0

# Database Configuration
DATABASE_URL=postgresql://reelranker:reelranker123@localhost:5432/reelranker

# YouTube API Configuration
YOUTUBE_API_KEY=your_youtube_api_key_here

# AI/ML Configuration
OPENAI_API_KEY=your_openai_api_key_here
MODEL_NAME=gpt-3.5-turbo

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Security Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=development
DEBUG=true
```

## Troubleshooting

### Database Connection Issues
```bash
# Check if containers are running
docker ps

# Restart containers
cd deployment
docker-compose restart

# Check logs
docker-compose logs postgres
```

### Migration Issues
```bash
# Reset migrations
alembic downgrade base
alembic upgrade head
```

### Port Conflicts
If ports 5432 or 6379 are in use:
```bash
# Stop existing services
sudo lsof -ti:5432 | xargs kill -9
sudo lsof -ti:6379 | xargs kill -9
```

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
flake8 .
```

### Database Management
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```
