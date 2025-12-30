"""Common models for request and response validation."""
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether Career ML model is loaded")
    clip_loaded: bool = Field(default=False, description="Whether CLIP model is loaded")


class ErrorResponse(BaseModel):
    """Error response model."""
    
    detail: str = Field(..., description="Error detail message")
