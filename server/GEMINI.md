# Project Overview

This project consists of two main components:

## 1. FastAPI ML Server (`fastapi_server/`)

A professional FastAPI server providing ML-powered APIs for CLIP image comparison and career recommendation.

### Features
- **CLIP Image Comparison**: Compare images using OpenAI's CLIP model with optional text tag matching
- **Career Recommendation**: ML-powered career/course recommendations based on student profiles
- **RESTful API**: Clean, versioned API endpoints (`/api/v1/...`) with automatic OpenAPI documentation
- **Production Ready**: Proper error handling, logging, singleton services, and configuration management

### Project Structure
```
fastapi_server/
├── app/
│   ├── api/v1/          # API endpoints (clip.py, career.py)
│   ├── config/          # Settings with Pydantic
│   ├── core/            # Exceptions, logging
│   ├── models/          # Pydantic models for validation
│   ├── services/        # Business logic (CLIP, Career services)
│   └── utils/           # File handling utilities
├── ml_models/           # ML model storage
├── requirements.txt     # Python dependencies
└── .env                 # Environment configuration
```

### Building and Running

#### Setup
```bash
cd fastapi_server
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

#### Running
```bash
# Development (auto-reload)
python -m uvicorn app.main:app --reload --port 8000

# Production
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Server runs on http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 2. Node.js Server (`server/`)

A Node.js/Express server that integrates with the FastAPI ML server for image comparison functionality.

### Building and Running

#### Installation
```bash
cd server
npm install
```

#### Python Setup (for CLIP dependencies - only if not using FastAPI)
```bash
npm run python:setup
```

#### Running
```bash
# Development
npm run dev

# Production
npm run build
npm run start
```

The server starts on the port specified in `.env` (default is 5003).

### Integration with FastAPI

The Node.js CLIP controller (`src/controllers/clip.controller.ts`) now calls the FastAPI server instead of executing Python scripts directly:
- Endpoint: `POST http://localhost:5003/api/clip/compare`
- Proxies requests to FastAPI: `http://localhost:8000/api/v1/clip/compare`
- Handles file uploads and forwards them to FastAPI

**Environment Configuration**:
Add to `server/.env`:
```env
FASTAPI_URL=http://localhost:8000
```

## Development Conventions

### Code Style
- **FastAPI**: Python with type hints, Pydantic models, async/await
- **Node.js**: TypeScript with Express.js

### Testing

#### FastAPI Tests
```bash
cd fastapi_server
pytest tests/ -v
```

#### Node.js Tests
Not currently implemented.

### Project Architecture

**FastAPI** follows clean architecture principles:
- **Models**: Data validation with Pydantic
- **Services**: Business logic with singleton pattern for model management
- **API Routes**: Thin controllers that delegate to services
- **Config**: Centralized settings with environment variable support

**Node.js** integrates as an API gateway:
- Receives client requests
- Forwards ML-related requests to FastAPI
- Handles other business logic (database, authentication, etc.)

### Adding New ML Features

1. Create Pydantic models in `fastapi_server/app/models/`
2. Implement service class in `fastapi_server/app/services/`
3. Create API routes in `fastapi_server/app/api/v1/`
4. Update Node.js controllers to call new FastAPI endpoints (if needed)

## Dependencies

### FastAPI Server
- FastAPI 0.115.5
- PyTorch, CLIP, scikit-learn
- Pydantic for validation
- Uvicorn ASGI server

### Node.js Server
- Express 5.1.0
- TypeScript 5.9.2
- Multer for file uploads
- form-data for FastAPI integration
- Prisma ORM

## Notes

- Both servers should be running for full functionality
- FastAPI handles all ML operations (CLIP, career prediction)
- Node.js handles file uploads and forwards to FastAPI
- CLIP model is cached locally after first download
- Career recommendation models must be present in `research/Models/`
