"""FastAPI application for career recommendation and CLIP image comparison."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.core.logging import setup_logging, get_logger
from app.api.v1 import health, career, clip

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("Starting Career Recommendation & CLIP API...")
    
    try:
        # Import services to trigger model loading
        from app.services.career_service import career_predictor
        from app.services.clip_service import clip_service
        
        # Check if models loaded successfully
        if career_predictor.is_loaded():
            logger.info("✓ Career model loaded successfully")
        else:
            logger.warning("✗ Career model failed to load")
        
        if clip_service.is_loaded():
            logger.info("✓ CLIP model loaded successfully")
        else:
            logger.warning("✗ CLIP model failed to load")
            
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        # Don't raise - allow API to start even if models fail
    
    yield
    
    # Shutdown
    logger.info("Shutting down Career Recommendation & CLIP API...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="ML-powered career recommendation and CLIP image comparison API",
    version=settings.app_version,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(career.router, prefix="/api/v1")
app.include_router(clip.router, prefix="/api/v1")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Career Recommendation & CLIP API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "career_predict": "/api/v1/career/predict",
            "career_info": "/api/v1/career/info",
            "clip_compare": "/api/v1/clip/compare"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
