"""
Medical Image Preprocessing Pipeline
Handles DICOM, NIfTI, and standard image formats
"""

import numpy as np
import cv2
from PIL import Image
import pydicom
import nibabel as nib
from typing import Tuple, Optional, Union
import logging
from pathlib import Path


class MedicalImagePreprocessor:
    """Preprocessing pipeline for medical images"""
    
    def __init__(self, target_size: Tuple[int, int] = (224, 224)):
        self.target_size = target_size
        self.logger = logging.getLogger(__name__)
    
    def preprocess_image(self, image_path: Union[str, Path]) -> np.ndarray:
        """
        Main preprocessing function that handles different image formats
        """
        image_path = Path(image_path)
        
        try:
            if image_path.suffix.lower() == '.dcm':
                image = self._preprocess_dicom(image_path)
            elif image_path.suffix.lower() in ['.nii', '.gz']:
                image = self._preprocess_nifti(image_path)
            else:
                image = self._preprocess_standard_image(image_path)
            
            # Apply common preprocessing steps
            image = self._apply_common_preprocessing(image)
            
            return image
            
        except Exception as e:
            self.logger.error(f"Error preprocessing {image_path}: {e}")
            return self._create_blank_image()
    
    def _preprocess_dicom(self, path: Path) -> np.ndarray:
        """Preprocess DICOM images"""
        try:
            # Read DICOM file
            ds = pydicom.dcmread(str(path))
            
            # Get pixel array
            image = ds.pixel_array.astype(np.float32)
            
            # Handle different photometric interpretations
            if hasattr(ds, 'PhotometricInterpretation'):
                if ds.PhotometricInterpretation == 'MONOCHROME1':
                    image = np.max(image) - image
            
            # Normalize to 0-255 range
            image = self._normalize_image(image)
            
            # Convert to 3-channel if needed
            if len(image.shape) == 2:
                image = np.stack([image] * 3, axis=-1)
            
            return image.astype(np.uint8)
            
        except Exception as e:
            self.logger.error(f"DICOM preprocessing error: {e}")
            return self._create_blank_image()
    
    def _preprocess_nifti(self, path: Path) -> np.ndarray:
        """Preprocess NIfTI images"""
        try:
            # Load NIfTI image
            img = nib.load(str(path))
            image = img.get_fdata().astype(np.float32)
            
            # Handle 3D volumes - extract middle slice
            if len(image.shape) == 3:
                middle_slice = image.shape[2] // 2
                image = image[:, :, middle_slice]
            
            # Handle 4D volumes - extract middle slice from 3rd dimension
            elif len(image.shape) == 4:
                middle_slice = image.shape[2] // 2
                image = image[:, :, middle_slice, 0]  # Take first time point
            
            # Normalize
            image = self._normalize_image(image)
            
            # Convert to 3-channel
            image = np.stack([image] * 3, axis=-1)
            
            return image.astype(np.uint8)
            
        except Exception as e:
            self.logger.error(f"NIfTI preprocessing error: {e}")
            return self._create_blank_image()
    
    def _preprocess_standard_image(self, path: Path) -> np.ndarray:
        """Preprocess standard image formats (JPEG, PNG, etc.)"""
        try:
            # Load image
            image = cv2.imread(str(path))
            if image is None:
                # Try with PIL as fallback
                pil_image = Image.open(str(path))
                image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
            # Convert BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            return image
            
        except Exception as e:
            self.logger.error(f"Standard image preprocessing error: {e}")
            return self._create_blank_image()
    
    def _apply_common_preprocessing(self, image: np.ndarray) -> np.ndarray:
        """Apply common preprocessing steps"""
        # Resize to target size
        image = cv2.resize(image, self.target_size)
        
        # Convert to grayscale if needed (for some medical images)
        if len(image.shape) == 3 and image.shape[2] == 3:
            # Check if image is actually grayscale in RGB format
            if np.allclose(image[:, :, 0], image[:, :, 1]) and np.allclose(image[:, :, 1], image[:, :, 2]):
                image = image[:, :, 0:1]  # Keep single channel
                image = np.repeat(image, 3, axis=2)  # Convert back to 3-channel
        
        return image
    
    def _normalize_image(self, image: np.ndarray) -> np.ndarray:
        """Normalize image to 0-255 range"""
        # Remove outliers using percentile-based normalization
        p2, p98 = np.percentile(image, (2, 98))
        
        if p98 > p2:
            image = np.clip((image - p2) / (p98 - p2), 0, 1) * 255
        else:
            image = np.zeros_like(image)
        
        return image
    
    def _create_blank_image(self) -> np.ndarray:
        """Create a blank image as fallback"""
        return np.zeros((*self.target_size, 3), dtype=np.uint8)


class ScanTypeSpecificPreprocessor:
    """Scan-type specific preprocessing"""
    
    @staticmethod
    def preprocess_brain_scan(image: np.ndarray) -> np.ndarray:
        """Brain scan specific preprocessing"""
        # Apply brain-specific normalization
        if len(image.shape) == 3:
            # Convert to grayscale for brain scans
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            image = np.stack([gray] * 3, axis=-1)
        
        # Apply histogram equalization for better contrast
        if len(image.shape) == 3:
            for i in range(image.shape[2]):
                image[:, :, i] = cv2.equalizeHist(image[:, :, i])
        
        return image
    
    @staticmethod
    def preprocess_cardiac_scan(image: np.ndarray) -> np.ndarray:
        """Cardiac scan specific preprocessing"""
        # Apply cardiac-specific enhancements
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            image = np.stack([gray] * 3, axis=-1)
        
        # Apply CLAHE for better contrast
        if len(image.shape) == 3:
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            for i in range(image.shape[2]):
                image[:, :, i] = clahe.apply(image[:, :, i])
        
        return image
    
    @staticmethod
    def preprocess_chest_scan(image: np.ndarray) -> np.ndarray:
        """Chest scan specific preprocessing"""
        # Chest X-rays are typically grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            image = np.stack([gray] * 3, axis=-1)
        
        # Apply lung-specific preprocessing
        # Remove background noise
        kernel = np.ones((3, 3), np.uint8)
        if len(image.shape) == 3:
            for i in range(image.shape[2]):
                image[:, :, i] = cv2.morphologyEx(image[:, :, i], cv2.MORPH_CLOSE, kernel)
        
        return image
    
    @staticmethod
    def preprocess_bone_scan(image: np.ndarray) -> np.ndarray:
        """Bone scan specific preprocessing"""
        # Bone X-rays are typically grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            image = np.stack([gray] * 3, axis=-1)
        
        # Apply bone-specific enhancement
        # Enhance edges for better bone visibility
        if len(image.shape) == 3:
            for i in range(image.shape[2]):
                # Apply unsharp masking
                blurred = cv2.GaussianBlur(image[:, :, i], (0, 0), 2.0)
                image[:, :, i] = cv2.addWeighted(image[:, :, i], 1.5, blurred, -0.5, 0)
        
        return image


def get_preprocessor(scan_type: str, target_size: Tuple[int, int] = (224, 224)):
    """Get appropriate preprocessor for scan type"""
    base_preprocessor = MedicalImagePreprocessor(target_size)
    
    def preprocess_with_type_specific(image_path):
        # Apply base preprocessing
        image = base_preprocessor.preprocess_image(image_path)
        
        # Apply scan-type specific preprocessing
        if scan_type == 'brain':
            image = ScanTypeSpecificPreprocessor.preprocess_brain_scan(image)
        elif scan_type == 'cardiac':
            image = ScanTypeSpecificPreprocessor.preprocess_cardiac_scan(image)
        elif scan_type == 'chest':
            image = ScanTypeSpecificPreprocessor.preprocess_chest_scan(image)
        elif scan_type == 'bone':
            image = ScanTypeSpecificPreprocessor.preprocess_bone_scan(image)
        
        return image
    
    return preprocess_with_type_specific
