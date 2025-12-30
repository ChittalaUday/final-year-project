"""CLIP image comparison API endpoints."""
from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path
import tempfile
import os

from app.models.clip import CLIPCompareResponse
from app.services.clip_service import clip_service
from app.core.exceptions import ModelNotLoadedError, PredictionError
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/clip", tags=["CLIP"])


@router.post("/compare", response_model=CLIPCompareResponse)
async def compare_images(
    image1: UploadFile = File(..., description="First image to compare"),
    image2: UploadFile = File(..., description="Second image to compare")
):
    """
    Compare two images using CLIP model and return similarity score.
    
    - **image1**: First image file (JPEG, PNG, etc.)
    - **image2**: Second image file (JPEG, PNG, etc.)
    
    Returns a similarity score between 0 and 1 (higher means more similar).
    """
    temp_files = []
    
    try:
        # Validate file types
        allowed_types = {"image/jpeg", "image/png", "image/jpg", "image/webp"}
        if image1.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type for image1: {image1.content_type}"
            )
        if image2.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type for image2: {image2.content_type}"
            )
        
        # Save uploaded files to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(image1.filename).suffix) as tmp1:
            content1 = await image1.read()
            tmp1.write(content1)
            temp1_path = tmp1.name
            temp_files.append(temp1_path)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(image2.filename).suffix) as tmp2:
            content2 = await image2.read()
            tmp2.write(content2)
            temp2_path = tmp2.name
            temp_files.append(temp2_path)
        
        # Compute similarity
        similarity = clip_service.compute_similarity(temp1_path, temp2_path)
        
        return CLIPCompareResponse(
            similarity=similarity,
            message="Images compared successfully"
        )
    
    except ModelNotLoadedError as e:
        raise HTTPException(
            status_code=503,
            detail=f"CLIP model not loaded: {str(e)}"
        )
    except PredictionError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"CLIP comparison error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to compare images: {str(e)}"
        )
    finally:
        # Clean up temporary files
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except Exception as e:
                logger.warning(f"Failed to delete temp file {temp_file}: {str(e)}")
