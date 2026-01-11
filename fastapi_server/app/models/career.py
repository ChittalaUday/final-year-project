"""Pydantic models for career prediction request and response validation."""

from typing import List
from pydantic import BaseModel, Field, field_validator


class CareerInput(BaseModel):
    """Input model for career prediction."""

    gender: str = Field(..., description="Gender (Male/Female)")
    interest: str = Field(..., description="Comma or semicolon separated interests")
    skills: str = Field(..., description="Comma or semicolon separated skills")
    grades: float = Field(..., ge=0, le=100, description="CGPA or Percentage (0-100)")

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v: str) -> str:
        """Validate gender input."""
        if v.lower() not in ["male", "female"]:
            raise ValueError("Gender must be 'Male' or 'Female'")
        return v.capitalize()

    @field_validator("interest", "skills")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        """Validate that interest and skills are not empty."""
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()

    @field_validator("grades")
    @classmethod
    def validate_grades(cls, v: float) -> float:
        """Validate grades are within reasonable range."""
        if v < 0 or v > 100:
            raise ValueError("Grades must be between 0 and 100")
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "gender": "Female",
                    "interest": "Cloud computing, Technology",
                    "skills": "Python, SQL, Java",
                    "grades": 85.0,
                }
            ]
        }
    }


class CoursePrediction(BaseModel):
    """Single course prediction with probability."""

    course: str = Field(..., description="Course name")
    probability: float = Field(..., ge=0, le=1, description="Prediction probability")


class CareerRecommendation(BaseModel):
    """Response model for career prediction."""

    predicted_course: str = Field(..., description="Top predicted course")
    confidence: float = Field(
        ..., ge=0, le=1, description="Prediction confidence score"
    )
    top_predictions: List[CoursePrediction] = Field(
        ..., description="Top 3 course predictions with probabilities"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "predicted_course": "B.Tech",
                    "confidence": 0.85,
                    "top_predictions": [
                        {"course": "B.Tech", "probability": 0.85},
                        {"course": "B.Sc", "probability": 0.10},
                        {"course": "MCA", "probability": 0.05},
                    ],
                }
            ]
        }
    }


class CareerFeedback(CareerInput):
    """Model for submitting career prediction feedback."""

    actual_course: str = Field(
        ..., description="The actual course the student took or is interested in"
    )


class CareerLists(BaseModel):
    """Response model for lists of valid options."""

    interests: List[str] = Field(..., description="List of valid interests")
    skills: List[str] = Field(..., description="List of valid skills")
    courses: List[str] = Field(..., description="List of valid courses")
