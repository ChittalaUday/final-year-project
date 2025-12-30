"""Career predictor service for loading models and making predictions."""
# Trigger reload to load new encoder files - mlb_interest.pkl and mlb_skills.pkl
import joblib
import numpy as np
from pathlib import Path
from typing import Dict, List
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor

from app.config import settings
from app.core.logging import get_logger
from app.core.exceptions import ModelNotLoadedError, PredictionError

logger = get_logger(__name__)


class CareerPredictor:
    """Handles model loading and career predictions."""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the predictor and load models."""
        if self._initialized:
            return
            
        self.model: RandomForestRegressor = None
        self.scaler: StandardScaler = None
        self.gender_encoder: LabelEncoder = None
        self.interest_encoder: MultiLabelBinarizer = None
        self.skills_encoder: MultiLabelBinarizer = None
        self._load_models()
        self._initialized = True
    
    def _load_models(self):
        """Load the trained models from disk."""
        try:
            # Load Random Forest model
            rf_path = settings.model_paths["random_forest"]
            if not rf_path.exists():
                raise FileNotFoundError(f"Model file not found: {rf_path}")
            self.model = joblib.load(rf_path)
            logger.info(f"✓ Loaded Random Forest model from {rf_path}")
            
            # Load Standard Scaler
            scaler_path = settings.model_paths["scaler"]
            if not scaler_path.exists():
                raise FileNotFoundError(f"Scaler file not found: {scaler_path}")
            self.scaler = joblib.load(scaler_path)
            logger.info(f"✓ Loaded Standard Scaler from {scaler_path}")
            
            # Gender encoder: NOT saved during training (le.pkl was overwritten with course labels)
            # Always initialize fresh
            self._initialize_gender_encoder()
            
            # MultiLabelBinarizer: Load the properly fitted encoders
            # (created from actual training data to match exact feature counts)
            mlb_interest_path = settings.models_dir / "mlb_interest.pkl"
            mlb_skills_path = settings.models_dir / "mlb_skills.pkl"
            
            if mlb_interest_path.exists() and mlb_skills_path.exists():
                self.interest_encoder = joblib.load(mlb_interest_path)
                self.skills_encoder = joblib.load(mlb_skills_path)
                logger.info(f"✓ Loaded MultiLabelBinarizers ({len(self.interest_encoder.classes_)} interests, {len(self.skills_encoder.classes_)} skills)")
            else:
                logger.warning("MLB encoders not found, initializing with settings (may cause feature mismatch)")
                self._initialize_mlb_encoders()
            
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            raise ModelNotLoadedError(f"Error loading models: {str(e)}")
    
    def _initialize_gender_encoder(self):
        """Initialize gender encoder to match training data."""
        self.gender_encoder = LabelEncoder()
        # Fit with classes in the same order as training (alphabetical: Female, Male)
        self.gender_encoder.fit(["Female", "Male"])
        logger.info("✓ Initialized gender encoder with classes: ['Female', 'Male']")
    
    def _initialize_mlb_encoders(self):
        """Initialize MultiLabelBinarizer encoders (fallback if not loaded from file)."""
        # Interest encoder - fit on all valid interests
        self.interest_encoder = MultiLabelBinarizer()
        self.interest_encoder.fit([settings.valid_interests])
        
        # Skills encoder - fit on all valid skills
        self.skills_encoder = MultiLabelBinarizer()
        self.skills_encoder.fit([settings.valid_skills])
        
        logger.info("✓ Initialized interest and skills encoders")
    
    def _parse_text_list(self, text: str) -> List[str]:
        """Parse comma/semicolon separated text into list of lowercase items."""
        # Replace semicolons with commas and split
        items = text.replace(';', ',').split(',')
        # Clean and lowercase each item
        return [item.lower().strip() for item in items if item.strip()]
    
    def _preprocess_input(self, gender: str, interest: str, skills: str, grades: float) -> np.ndarray:
        """Preprocess input data to match training format."""
        try:
            # Encode gender
            gender_encoded = self.gender_encoder.transform([gender])[0]
            
            # Parse and encode interests
            interest_list = self._parse_text_list(interest)
            interest_encoded = self.interest_encoder.transform([interest_list])[0]
            
            # Parse and encode skills
            skills_list = self._parse_text_list(skills)
            skills_encoded = self.skills_encoder.transform([skills_list])[0]
            
            # Combine all features
            # Order: gender, grades, interest features, skill features
            features = np.concatenate([
                [gender_encoded],
                [grades],
                interest_encoded,
                skills_encoded
            ])
            
            # Reshape for scaling
            features = features.reshape(1, -1)
            
            # Apply standard scaling
            features_scaled = self.scaler.transform(features)
            
            return features_scaled
        except Exception as e:
            raise PredictionError(f"Error preprocessing input: {str(e)}")
    
    def predict(self, gender: str, interest: str, skills: str, grades: float) -> Dict:
        """
        Make career prediction based on input features.
        
        Args:
            gender: User's gender (Male/Female)
            interest: Comma/semicolon separated interests
            skills: Comma/semicolon separated skills
            grades: CGPA or percentage
        
        Returns:
            Dictionary with predicted course and confidence scores
        """
        if not self.is_loaded():
            raise ModelNotLoadedError("Models not loaded properly")
        
        try:
            # Preprocess input
            features = self._preprocess_input(gender, interest, skills, grades)
            
            # Make prediction
            predicted_course_code = self.model.predict(features)[0]
            
            # Round to nearest integer (course code)
            predicted_course_code = int(round(predicted_course_code))
            
            # Ensure the predicted code is within valid range
            if predicted_course_code < 0:
                predicted_course_code = 0
            elif predicted_course_code >= len(settings.course_mapping):
                predicted_course_code = len(settings.course_mapping) - 1
            
            # Get course name
            predicted_course = settings.course_mapping.get(predicted_course_code, "Unknown")
            
            # For Random Forest, we can get prediction probabilities from trees
            # Get predictions from all trees
            tree_predictions = np.array([
                tree.predict(features)[0] for tree in self.model.estimators_
            ])
            
            # Calculate confidence as inverse of standard deviation
            # Lower std = higher confidence
            std_dev = np.std(tree_predictions)
            confidence = 1.0 / (1.0 + std_dev)
            
            # Get top 3 predictions by analyzing tree predictions
            unique_predictions, counts = np.unique(
                np.round(tree_predictions).astype(int), 
                return_counts=True
            )
            
            # Sort by count (descending)
            sorted_indices = np.argsort(counts)[::-1]
            top_courses = []
            
            for idx in sorted_indices[:3]:
                course_code = unique_predictions[idx]
                probability = counts[idx] / len(tree_predictions)
                
                # Ensure course code is valid
                if 0 <= course_code < len(settings.course_mapping):
                    top_courses.append({
                        "course": settings.course_mapping[course_code],
                        "probability": float(probability)
                    })
            
            # Ensure we have at least 3 predictions
            while len(top_courses) < 3:
                top_courses.append({
                    "course": "N/A",
                    "probability": 0.0
                })
            
            return {
                "predicted_course": predicted_course,
                "confidence": float(confidence),
                "top_predictions": top_courses[:3]
            }
        except PredictionError:
            raise
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise PredictionError(f"Prediction failed: {str(e)}")
    
    def is_loaded(self) -> bool:
        """Check if models are loaded successfully."""
        return (
            self.model is not None and
            self.scaler is not None and
            self.gender_encoder is not None and
            self.interest_encoder is not None and
            self.skills_encoder is not None
        )


# Global singleton instance
career_predictor = CareerPredictor()
