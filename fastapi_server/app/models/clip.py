"""Pydantic models for CLIP image comparison."""
from typing import Optional
from pydantic import BaseModel, Field


class ImageSimilarity(BaseModel):
    """Image similarity score with optional metadata."""
    
    similarity_score: float = Field(
        ..., 
        ge=0.0, 
        le=1.0,
        description="Cosine similarity score between images (0-1)"
    )
    image1_path: Optional[str] = Field(None, description="Path to first image")
    image2_path: Optional[str] = Field(None, description="Path to second image")


class CLIPCompareResponse(BaseModel):
    """Response for CLIP image comparison."""
    
    similarity: float = Field(
        ..., 
        ge=0.0, 
        le=1.0,
        description="Similarity score between the two images"
    )
    message: str = Field(default="Images compared successfully")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "similarity": 0.87,
                    "message": "Images compared successfully"
                }
            ]
        }
    }
