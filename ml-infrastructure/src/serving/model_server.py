"""
FastAPI Model Server for Medical Scan Analysis
Serves trained models for Brain, Cardiac, Chest, and Bone scans
"""

import os
import io
import base64
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
import cv2
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Import our models and preprocessing
from ..models.medical_models import create_model
from ..data.preprocessing import get_preprocessor


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PredictionRequest(BaseModel):
    """Request model for predictions"""
    image_data: str  # Base64 encoded image
    scan_type: str
    confidence_threshold: Optional[float] = 0.5


class PredictionResponse(BaseModel):
    """Response model for predictions"""
    predictions: List[Dict[str, Any]]
    confidence: float
    scan_type: str
    processing_time: float
    model_version: str


class MedicalModelServer:
    """Medical AI Model Server"""
    
    def __init__(self, models_dir: str = "models"):
        self.app = FastAPI(
            title="Medical Scan Analysis API",
            description="AI-powered medical scan analysis for Brain, Cardiac, Chest, and Bone scans",
            version="1.0.0"
        )
        
        self.models_dir = Path(models_dir)
        self.models = {}
        self.preprocessors = {}
        self.model_configs = {}
        
        # Setup CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Load models
        self.load_models()
        
        # Setup routes
        self.setup_routes()
    
    def load_models(self):
        """Load all trained models"""
        scan_types = ['brain', 'cardiac', 'chest', 'bone']
        
        for scan_type in scan_types:
            model_path = self.models_dir / scan_type / f"{scan_type}_best_model.pth"
            
            if model_path.exists():
                try:
                    self.load_model(scan_type, model_path)
                    logger.info(f"Loaded {scan_type} model successfully")
                except Exception as e:
                    logger.error(f"Failed to load {scan_type} model: {e}")
            else:
                logger.warning(f"No model found for {scan_type} at {model_path}")
    
    def load_model(self, scan_type: str, model_path: Path):
        """Load a specific model"""
        # Load checkpoint
        checkpoint = torch.load(model_path, map_location='cpu')
        
        # Create model architecture
        model = create_model(
            scan_type=scan_type,
            num_classes=len(self.get_classes(scan_type)),
            model_name='efficientnet-b4',  # Default architecture
            pretrained=False
        )
        
        # Load weights
        model.load_state_dict(checkpoint['model_state_dict'])
        model.eval()
        
        # Store model
        self.models[scan_type] = model
        self.model_configs[scan_type] = checkpoint.get('config', {})
        
        # Create preprocessor
        self.preprocessors[scan_type] = get_preprocessor(scan_type)
        
        logger.info(f"Loaded {scan_type} model with {checkpoint.get('epoch', 'unknown')} epochs")
    
    def get_classes(self, scan_type: str) -> List[str]:
        """Get class names for scan type"""
        class_mapping = {
            'brain': ['normal', 'tumor', 'stroke', 'hemorrhage', 'atrophy'],
            'cardiac': ['normal', 'cardiomyopathy', 'valvular_disease', 'coronary_disease', 'arrhythmia'],
            'chest': ['normal', 'pneumonia', 'covid', 'tuberculosis', 'lung_cancer', 'pneumothorax'],
            'bone': ['normal', 'fracture', 'osteoporosis', 'arthritis', 'tumor']
        }
        return class_mapping.get(scan_type, ['unknown'])
    
    def setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/")
        async def root():
            return {
                "message": "Medical Scan Analysis API",
                "version": "1.0.0",
                "available_models": list(self.models.keys()),
                "endpoints": [
                    "/predict",
                    "/predict/file",
                    "/health",
                    "/models/status"
                ]
            }
        
        @self.app.get("/health")
        async def health_check():
            return {
                "status": "healthy",
                "models_loaded": len(self.models),
                "available_scan_types": list(self.models.keys())
            }
        
        @self.app.get("/models/status")
        async def models_status():
            status = {}
            for scan_type, model in self.models.items():
                status[scan_type] = {
                    "loaded": True,
                    "classes": self.get_classes(scan_type),
                    "model_path": str(self.models_dir / scan_type / f"{scan_type}_best_model.pth")
                }
            return status
        
        @self.app.post("/predict", response_model=PredictionResponse)
        async def predict(request: PredictionRequest):
            """Predict using base64 encoded image"""
            return await self._predict(
                image_data=request.image_data,
                scan_type=request.scan_type,
                confidence_threshold=request.confidence_threshold
            )
        
        @self.app.post("/predict/file", response_model=PredictionResponse)
        async def predict_file(
            file: UploadFile = File(...),
            scan_type: str = Form(...),
            confidence_threshold: float = Form(0.5)
        ):
            """Predict using uploaded file"""
            # Read file
            contents = await file.read()
            
            # Convert to base64
            image_data = base64.b64encode(contents).decode('utf-8')
            
            return await self._predict(
                image_data=f"data:{file.content_type};base64,{image_data}",
                scan_type=scan_type,
                confidence_threshold=confidence_threshold
            )
    
    async def _predict(
        self,
        image_data: str,
        scan_type: str,
        confidence_threshold: float = 0.5
    ) -> PredictionResponse:
        """Main prediction function"""
        import time
        start_time = time.time()
        
        try:
            # Validate scan type
            if scan_type not in self.models:
                raise HTTPException(
                    status_code=400,
                    detail=f"Model not available for scan type: {scan_type}"
                )
            
            # Load and preprocess image
            image = self._load_image_from_base64(image_data)
            preprocessed_image = self._preprocess_image(image, scan_type)
            
            # Get model prediction
            predictions = self._get_model_prediction(preprocessed_image, scan_type)
            
            # Filter predictions by confidence threshold
            filtered_predictions = [
                pred for pred in predictions
                if pred['confidence'] >= confidence_threshold
            ]
            
            # Calculate overall confidence
            overall_confidence = max([pred['confidence'] for pred in predictions])
            
            processing_time = time.time() - start_time
            
            return PredictionResponse(
                predictions=filtered_predictions,
                confidence=overall_confidence,
                scan_type=scan_type,
                processing_time=processing_time,
                model_version="1.0.0"
            )
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    def _load_image_from_base64(self, image_data: str) -> np.ndarray:
        """Load image from base64 string"""
        try:
            # Remove data URL prefix if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode base64
            image_bytes = base64.b64decode(image_data)
            
            # Load image
            image = Image.open(io.BytesIO(image_bytes))
            image = np.array(image)
            
            return image
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image data: {e}")
    
    def _preprocess_image(self, image: np.ndarray, scan_type: str) -> torch.Tensor:
        """Preprocess image for model input"""
        try:
            # Get preprocessor
            preprocessor = self.preprocessors[scan_type]
            
            # Apply preprocessing
            processed_image = preprocessor(image)
            
            # Convert to tensor and add batch dimension
            if isinstance(processed_image, np.ndarray):
                processed_image = torch.from_numpy(processed_image)
            
            # Ensure correct shape: (C, H, W)
            if len(processed_image.shape) == 3:
                processed_image = processed_image.permute(2, 0, 1)
            
            # Add batch dimension: (1, C, H, W)
            processed_image = processed_image.unsqueeze(0).float()
            
            return processed_image
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image preprocessing failed: {e}")
    
    def _get_model_prediction(self, image_tensor: torch.Tensor, scan_type: str) -> List[Dict[str, Any]]:
        """Get model prediction"""
        try:
            model = self.models[scan_type]
            classes = self.get_classes(scan_type)
            
            # Get prediction
            with torch.no_grad():
                outputs = model(image_tensor)
                
                if isinstance(outputs, dict):
                    logits = outputs['logits']
                else:
                    logits = outputs
                
                # Get probabilities
                probabilities = F.softmax(logits, dim=1)
                probs = probabilities[0].cpu().numpy()
                
                # Create predictions
                predictions = []
                for i, (class_name, prob) in enumerate(zip(classes, probs)):
                    predictions.append({
                        'class': class_name,
                        'confidence': float(prob),
                        'class_id': i
                    })
                
                # Sort by confidence
                predictions.sort(key=lambda x: x['confidence'], reverse=True)
                
                return predictions
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Model prediction failed: {e}")


def create_app(models_dir: str = "models") -> FastAPI:
    """Create FastAPI application"""
    server = MedicalModelServer(models_dir)
    return server.app


def main():
    """Main function to run the server"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Medical Model Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to')
    parser.add_argument('--models-dir', default='models', help='Directory containing trained models')
    parser.add_argument('--workers', type=int, default=1, help='Number of workers')
    
    args = parser.parse_args()
    
    app = create_app(args.models_dir)
    
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        workers=args.workers
    )


if __name__ == "__main__":
    main()
