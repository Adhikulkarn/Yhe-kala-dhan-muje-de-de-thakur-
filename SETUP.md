# Setup and Deployment Guide

## Overview

This is a full-stack AML (Anti-Money Laundering) detection system with:
- **Backend**: Django REST API with hybrid graph-based AML detection
- **Frontend**: React application for graph visualization and wallet risk analysis

## Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn

## Development Setup

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file for configuration
cp ../.env.example .env
# Edit .env with your configuration
```

### 2. Backend Configuration

Create `.env` file in the backend directory:

```bash
# Generate a secure secret key:
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Copy to .env:
DJANGO_SECRET_KEY=your-generated-key-here
DEBUG=true
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 3. Run Backend Server

```bash
cd backend/server

# Run migrations (first time only)
python manage.py migrate

# Start development server
python manage.py runserver
```

The API will be available at: `http://127.0.0.1:8000`

### 4. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at: `http://localhost:5173`

## API Endpoints

- `GET /api/health/` - Health check
- `POST /api/upload-csv/` - Upload transaction CSV
- `POST /api/analyze/` - Run AML analysis
- `GET /api/graph/` - Get transaction graph visualization data
- `GET /api/risk-scores/` - Get detailed risk scores per wallet
- `GET /api/final-risk/` - Get final fused risk scores

## CSV Format

### Crypto AML Mode

```csv
Source_Wallet_ID,Dest_Wallet_ID,Timestamp,Amount,Token_Type
0x123...abc,0x456...def,2024-01-15 10:30:00,1.5,ETH
...
```

### Banking AML Mode

```csv
src_id,dst_id,amount,additional_field
A001,B001,5000,...
...
```

## Production Deployment

### Security Checklist

- [ ] Set `DEBUG=false` in `.env`
- [ ] Generate strong `DJANGO_SECRET_KEY`
- [ ] Set `ALLOWED_HOSTS` to production domain
- [ ] Set `CORS_ALLOWED_ORIGINS` to frontend domain
- [ ] Use HTTPS in production
- [ ] Configure database (not SQLite)
- [ ] Set up environment variables securely

### Using Environment Variables

The system reads configuration from environment variables:

```bash
export DJANGO_SECRET_KEY="your-secret-key"
export DEBUG="false"
export ALLOWED_HOSTS="example.com,www.example.com"
export CORS_ALLOWED_ORIGINS="https://example.com,https://www.example.com"
```

### Docker Deployment (Optional)

Create `Dockerfile` for backend:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

CMD ["python", "server/manage.py", "runserver", "0.0.0.0:8000"]
```

### Using gunicorn for Production

```bash
pip install gunicorn
gunicorn server.wsgi:application --bind 0.0.0.0:8000
```

## Testing

### Backend Tests

```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## Troubleshooting

### CORS Errors

If you see CORS errors, verify:
1. Frontend URL is in `CORS_ALLOWED_ORIGINS`
2. Backend is running
3. Check `.env` configuration

### CSV Upload Fails

Ensure:
1. CSV has required columns for selected mode
2. File is valid UTF-8 encoding
3. File is under 10MB
4. Column headers match exactly (case-sensitive)

### Graph Fails to Load

Check:
1. Analysis completed successfully
2. API is returning valid data
3. Browser console for JavaScript errors
4. Network tab for API response status

## Architecture

```
Frontend (React)
    ↓
Backend (Django REST API)
    ↓
AML Pipeline
    ├─ Graph Building
    ├─ Feature Extraction
    ├─ Pattern Detection
    ├─ Risk Scoring
    └─ GNN Inference (optional)
```

## API Error Response Codes

- `400` - Invalid input (bad CSV, missing data)
- `404` - Resource not found
- `500` - Server error during analysis
- `200` - Success

## Support and Documentation

- See README.md for project overview
- Check backend/server/api/views.py for endpoint details
- Review core modules in backend/core/ for algorithm documentation
