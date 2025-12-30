# FastAPI ML Server

A professional FastAPI server providing ML-powered APIs for CLIP image comparison and career recommendation.

## Features

- **CLIP Image Comparison**: Compare images using OpenAI's CLIP model with optional text tag matching
- **Career Recommendation**: ML-powered career/course recommendations based on student profiles
- **RESTful API**: Clean, versioned API endpoints with automatic OpenAPI documentation
- **Production Ready**: Proper error handling, logging, and configuration management

## Project Structure

```
fastapi_server/
├── app/
│   ├── api/              # API endpoints
│   │   ├── deps.py       # Shared dependencies
│   │   └── v1/           # API version 1
│   ├── config/           # Configuration
│   ├── core/             # Core utilities
│   ├── models/           # Pydantic models
│   ├── services/         # Business logic
│   └── utils/            # Helper functions
├── ml_models/            # ML model storage
├── uploads/              # Temporary uploads
├── requirements.txt      # Python dependencies
└── .env                  # Environment configuration
```

## Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment** (optional):
   - Copy `.env.example` to `.env` if needed
   - Modify settings in `.env` as required

### Running the Server

**Development mode** (with auto-reload):
```bash
python -m uvicorn app.main:app --reload --port 8000
```

**Production mode**:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The server will start on http://localhost:8000

## API Documentation

Once the server is running, access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### CLIP Image Comparison

#### `POST /api/v1/clip/compare`

Compare two images using CLIP model.

**Request**:
- `image1` (file): First image
- `image2` (file): Second image  
- `tag` (optional string): Text tag for semantic comparison

**Response**:
```json
{
  "image_similarity": 0.85,
  "text_similarity": 0.72,
  "decision": "Images and text match",
  "details": "Image similarity: 0.8500, Text similarity ('cat'): 0.7200...",
  "is_image_similar": true,
  "is_text_similar": true,
  "thresholds": {
    "image": 0.3,
    "text": 0.3,
    "image_strict": 0.8
  }
}
```

#### `GET /api/v1/clip/info`

Get CLIP API information.

### Career Recommendation

#### `POST /api/v1/career/predict`

Get career/course recommendation.

**Request**:
```json
{
  "gender": "Female",
  "interest": "Cloud computing, Technology",
  "skills": "Python, SQL, Java",
  "grades": 85.0
}
```

**Response**:
```json
{
  "predicted_course": "B.Tech",
  "confidence": 0.85,
  "top_predictions": [
    {"course": "B.Tech", "probability": 0.85},
    {"course": "B.Sc", "probability": 0.10},
    {"course": "MCA", "probability": 0.05}
  ]
}
```

#### `GET /api/v1/career/info`

Get career recommendation API information.

### Health & Status

#### `GET /health`

Check service health status.

**Response**:
```json
{
  "status": "healthy",
  "services": {
    "career_recommendation": {
      "status": "healthy",
      "model_loaded": true
    },
    "clip": {
      "status": "healthy",
      "model_loaded": true
    }
  }
}
```

## Configuration

Edit `.env` to configure:

- **Server settings**: Host, port, debug mode
- **CORS origins**: Allowed origins for cross-origin requests
- **Model paths**: Locations of ML models
- **Upload settings**: Max file size, allowed formats
- **CLIP thresholds**: Similarity thresholds

## Development

### Code Structure

- **Models** (`app/models/`): Pydantic models for request/response validation
- **Services** (`app/services/`): Business logic and ML model handling
- **API Routes** (`app/api/v1/`): FastAPI route handlers
- **Config** (`app/config/`): Application settings management
- **Core** (`app/core/`): Shared utilities (exceptions, logging)

### Adding New Endpoints

1. Create Pydantic models in `app/models/`
2. Implement business logic in `app/services/`
3. Create route handlers in `app/api/v1/`
4. Register router in `app/api/v1/__init__.py`

## Troubleshooting

### Model Loading Errors

Ensure model files exist in the paths specified in `.env`:
- Career models: `../research/Models/rf.sav` and `sc.sav`
- CLIP model will be downloaded automatically on first run

### Port Already in Use

Change the port in `.env` or pass `--port` flag:
```bash
uvicorn app.main:app --port 8001
```

### CORS Issues

Add your origin to `CORS_ORIGINS` in `.env`.

## License

ISC
