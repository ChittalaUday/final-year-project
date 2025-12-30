"""Health check endpoint."""
from fastapi import APIRouter

from app.models.common import HealthResponse
from app.services.career_service import career_predictor
from app.services.clip_service import clip_service

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify service status."""
    career_loaded = career_predictor.is_loaded()
    clip_loaded = clip_service.is_loaded()
    
    all_healthy = career_loaded and clip_loaded
    
    return HealthResponse(
        status="healthy" if all_healthy else "degraded",
        model_loaded=career_loaded,
        clip_loaded=clip_loaded
    )
