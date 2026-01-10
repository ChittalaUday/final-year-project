# 🧠 FastAPI ML Server or AI / ML Service

Professional AI/ML microservice providing career recommendations and image analysis capabilities using FastAPI. This service operates as the intelligence layer of the Skill Compass platform.

## 1️⃣ Overview

**Purpose**: To handle all machine learning operations separately from the main business logic.  
**Role**: Receives computation-heavy requests (like image comparison or career prediction) from the Node.js backend, processes them using loaded models, and returns structured data.

## 2️⃣ Tech Stack

*   **Language**: Python 3.10+
*   **Framework**: FastAPI (High-performance web framework)
*   **ML Libraries**:
    *   `torch`, `torchvision`, `clip-by-openai` (Image analysis)
    *   `scikit-learn`, `pandas`, `numpy` (Career data analysis)
*   **Server**: Uvicorn (ASGI)
*   **Validation**: Pydantic

## 3️⃣ Folder Structure

```
fastapi_server/
├── app/
│   ├── api/v1/          # Endpoints (career.py, clip.py, health.py)
│   ├── core/            # Logging, exceptions, shared logic
│   ├── models/          # Pydantic data schemas (Request/Response)
│   ├── services/        # Business logic & Model loading (Singleton patterns)
│   ├── utils/           # Helper functions
│   ├── config.py        # Settings management
│   └── main.py          # Application entry point
├── ml_models/           # Local cache for CLIP models
├── requirements.txt     # Python dependencies
└── .env.example         # Template for environment variables
```

## 4️⃣ Current Features (Implemented)

*   **Career Prediction API**: Recommends careers based on student academic performance and interests (using Scikit-learn).
*   **CLIP Image Comparison**: Compares similarity between two uploaded images (features extraction via OpenAI CLIP).
*   **Text-to-Image Matching**: Optional text tag support for checking image relevance to a concept.
*   **Standardized API Response**: Uniform JSON structure for success and error states.
*   **Model Caching**: Models are loaded once at startup for performance.
*   **Swagger/Redoc**: Automatic interactive documentation.

## 5️⃣ Partially Implemented / In Progress

*   **Advanced Analytics**: More detailed breakdown of career compatibility.
*   **Model Retraining Endpoint**: automated pipeline to update models with new data (Planned).

## 6️⃣ Environment Variables

Create a `.env` file in `fastapi_server/` based on `.env.example`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `FASTAPI_HOST` | Host to bind the server | `0.0.0.0` |
| `FASTAPI_PORT` | Port to run the server | `8000` |
| `CORS_ORIGINS` | Allowed frontend/backend origins | `http://localhost:3000,...` |
| `DEBUG` | Enable debug logs | `False` |
| `CAREER_MODEL_DIR` | Path to stored `.pkl` models | `../research/Models` |
| `CLIP_MODEL_CACHE_DIR` | Path to cache downloaded CLIP models | `./ml_models/clip` |
| `UPLOAD_DIR` | Temp directory for processing uploads | `./uploads` |

## 7️⃣ How to Run This Service

### Prerequisites
*   Python 3.10 or higher
*   RAM: ~4GB recommended (for loading CLIP/ML models)

### Setup
1.  Navigate to the directory:
    ```bash
    cd fastapi_server
    ```
2.  Create virtual environment:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    # source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure Environment:
    Copy `.env.example` to `.env` and adjust paths if necessary.

### Start Server
```bash
# Development (Auto-reload)
python -m uvicorn app.main:app --reload --port 8000
```
Server will be available at `http://localhost:8000`.

## 8️⃣ API / Integration Notes

*   **Communication**: This service typically sits behind the Node.js API Gateway.
*   **Docs**: Visit `http://localhost:8000/docs` for full Swagger UI.
*   **Health Check**: `GET /health` to verify if models are loaded.
*   **Flow**:
    *   Node.js receives User Request -> Forwards to FastAPI (`/api/v1/...`) -> FastAPI returns JSON -> Node.js forwards to Client.

## 9️⃣ Known Limitations

*   **Cold Start**: Model loading can take 10-20 seconds on initial startup.
*   **Memory Usage**: CLIP model is memory intensive; deploying on very small instances (<2GB RAM) may crash.
