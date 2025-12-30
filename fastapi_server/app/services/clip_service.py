"""Hybrid image comparison service using CLIP, SSIM, and structural methods."""
import torch
import clip
from PIL import Image
import numpy as np
import cv2
from typing import Tuple, Dict
from pathlib import Path
from skimage.metrics import structural_similarity as ssim

from app.core.logging import get_logger
from app.core.exceptions import ModelNotLoadedError, PredictionError

logger = get_logger(__name__)


class CLIPService:
    """Handles hybrid image comparison using multiple methods."""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the CLIP service and load model."""
        if self._initialized:
            return
            
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.preprocess = None
        self._load_model()
        self._initialized = True
    
    def _load_model(self):
        """Load the CLIP model."""
        try:
            logger.info("Loading CLIP model...")
            self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
            logger.info(f"✓ Loaded CLIP model on {self.device}")
        except Exception as e:
            logger.error(f"Error loading CLIP model: {str(e)}")
            raise ModelNotLoadedError(f"Error loading CLIP model: {str(e)}")
    
    def _load_image(self, image_path: str) -> Image.Image:
        """Load an image from path.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            PIL Image object
        """
        try:
            return Image.open(image_path).convert("RGB")
        except Exception as e:
            raise PredictionError(f"Error loading image {image_path}: {str(e)}")
    
    def _compute_clip_similarity(self, image1: Image.Image, image2: Image.Image) -> float:
        """Compute CLIP semantic similarity."""
        image1_preprocessed = self.preprocess(image1).unsqueeze(0).to(self.device)
        image2_preprocessed = self.preprocess(image2).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            image1_features = self.model.encode_image(image1_preprocessed)
            image2_features = self.model.encode_image(image2_preprocessed)
            
            # Normalize features
            image1_features = image1_features / image1_features.norm(dim=-1, keepdim=True)
            image2_features = image2_features / image2_features.norm(dim=-1, keepdim=True)
            
            # Compute cosine similarity
            similarity = (image1_features @ image2_features.T).item()
        
        return max(0.0, min(1.0, similarity))
    
    def _compute_structural_similarity(self, image1: Image.Image, image2: Image.Image) -> float:
        """Compute SSIM (Structural Similarity Index) for pixel-level comparison."""
        # Convert to grayscale numpy arrays
        img1_gray = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2GRAY)
        img2_gray = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2GRAY)
        
        # Resize to same dimensions
        target_size = (224, 224)
        img1_resized = cv2.resize(img1_gray, target_size)
        img2_resized = cv2.resize(img2_gray, target_size)
        
        # Compute SSIM
        score, _ = ssim(img1_resized, img2_resized, full=True)
        return max(0.0, min(1.0, score))
    
    def _compute_histogram_similarity(self, image1: Image.Image, image2: Image.Image) -> float:
        """Compute color histogram correlation."""
        img1_cv = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
        img2_cv = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)
        
        # Compute histograms
        hist1 = cv2.calcHist([img1_cv], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist2 = cv2.calcHist([img2_cv], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        
        # Normalize
        hist1 = cv2.normalize(hist1, hist1).flatten()
        hist2 = cv2.normalize(hist2, hist2).flatten()
        
        # Compute correlation
        correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        return max(0.0, min(1.0, correlation))
    
    def _compute_edge_similarity(self, image1: Image.Image, image2: Image.Image) -> float:
        """Compute edge-based similarity for outline comparison."""
        # Convert to grayscale
        img1_gray = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2GRAY)
        img2_gray = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2GRAY)
        
        # Resize to same dimensions
        target_size = (224, 224)
        img1_resized = cv2.resize(img1_gray, target_size)
        img2_resized = cv2.resize(img2_gray, target_size)
        
        # Apply Canny edge detection
        edges1 = cv2.Canny(img1_resized, 50, 150)
        edges2 = cv2.Canny(img2_resized, 50, 150)
        
        # Compute SSIM on edges
        score, _ = ssim(edges1, edges2, full=True)
        return max(0.0, min(1.0, score))
    
    def compute_similarity(self, image1_path: str, image2_path: str) -> float:
        """
        Compute hybrid similarity optimized for outline/drawing comparison.
        
        Combines:
        - CLIP semantic similarity (30%)
        - Structural similarity/SSIM (30%)
        - Edge similarity (30%)
        - Histogram similarity (10%)
        
        Args:
            image1_path: Path to first image (reference/outline)
            image2_path: Path to second image (drawn image)
            
        Returns:
            Weighted similarity score (0-1, higher is more similar)
        """
        if not self.is_loaded():
            raise ModelNotLoadedError("CLIP model not loaded")
        
        try:
            # Load images
            image1 = self._load_image(image1_path)
            image2 = self._load_image(image2_path)
            
            # Compute different similarity metrics
            clip_sim = self._compute_clip_similarity(image1, image2)
            structural_sim = self._compute_structural_similarity(image1, image2)
            edge_sim = self._compute_edge_similarity(image1, image2)
            hist_sim = self._compute_histogram_similarity(image1, image2)
            
            # Weighted combination (optimized for outline/drawing comparison)
            # Higher weight on structural and edge similarity for shape matching
            similarity = (
                0.30 * clip_sim +          # Semantic understanding
                0.30 * structural_sim +     # Pixel-level structure
                0.30 * edge_sim +           # Shape/outline matching
                0.10 * hist_sim             # Color similarity
            )
            
            logger.info(f"Similarity breakdown - CLIP: {clip_sim:.3f}, SSIM: {structural_sim:.3f}, "
                       f"Edge: {edge_sim:.3f}, Hist: {hist_sim:.3f}, Final: {similarity:.3f}")
            
            return float(similarity)
            
        except PredictionError:
            raise
        except Exception as e:
            logger.error(f"Error computing similarity: {str(e)}")
            raise PredictionError(f"Failed to compute image similarity: {str(e)}")
    
    def is_loaded(self) -> bool:
        """Check if CLIP model is loaded successfully."""
        return self.model is not None and self.preprocess is not None


# Global singleton instance
clip_service = CLIPService()
