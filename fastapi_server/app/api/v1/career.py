"""Career recommendation API endpoints."""
from fastapi import APIRouter, HTTPException

from app.models.career import CareerInput, CareerRecommendation, CoursePrediction
from app.services.career_service import career_predictor
from app.core.exceptions import ModelNotLoadedError, PredictionError
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/career", tags=["Career"])


@router.post("/predict", response_model=CareerRecommendation)
async def predict_career(input_data: CareerInput):
    """
    Predict career/course recommendation based on student profile.
    
    - **gender**: Student's gender (Male/Female)
    - **interest**: Comma or semicolon separated interests
    - **skills**: Comma or semicolon separated skills
    - **grades**: CGPA or percentage (0-100)
    
    Returns the predicted course along with confidence score and top 3 predictions.
    """
    try:
        # Make prediction
        result = career_predictor.predict(
            gender=input_data.gender,
            interest=input_data.interest,
            skills=input_data.skills,
            grades=input_data.grades
        )
        
        # Convert to response model
        return CareerRecommendation(
            predicted_course=result["predicted_course"],
            confidence=result["confidence"],
            top_predictions=[
                CoursePrediction(**pred) for pred in result["top_predictions"]
            ]
        )
    
    except ModelNotLoadedError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Model not loaded: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PredictionError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@router.get("/info")
async def get_info():
    """Get information about the career recommendation model."""
    return {
        "model_type": "Random Forest Regressor",
        "features": [
            "gender",
            "interest (multi-hot encoded)",
            "skills (multi-hot encoded)",
            "grades"
        ],
        "preprocessing": [
            "Label encoding for gender",
            "Multi-label binarization for interests and skills",
            "Standard scaling for all features"
        ],
        "output": "Course recommendation with confidence scores"
    }
