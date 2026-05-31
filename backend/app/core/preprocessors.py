import numpy as np
import cv2
from PIL import Image
import logging
from pathlib import Path

# Try to import medical imaging libraries, handle ImportError for fallback
try:
    import pydicom
except ImportError:
    pydicom = None

try:
    import nibabel as nib
except ImportError:
    nib = None

class MedicalImagePreprocessor:
    """
    Core pipeline to ingest, clean, standardize, and enhance medical scans
    supporting DICOM, NIfTI, PNG, and JPEG inputs.
    """
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def load_and_preprocess(self, file_path, scan_type, target_size=(224, 224)):
        """
        Ingests image files, standardizes channels, applies scan-specific 
        enhancements, and returns a normalized NumPy array.
        """
        path = Path(file_path)
        
        try:
            # 1. Ingest base format
            if path.suffix.lower() == '.dcm':
                img_array = self._read_dicom(path)
            elif path.suffix.lower() in ['.nii', '.gz']:
                img_array = self._read_nifti(path)
            else:
                img_array = self._read_standard(path)
                
            # 2. Enhance structures based on clinical scan type
            enhanced = self._apply_enhancements(img_array, scan_type)
            
            # 3. Standardize dimensions
            resized = cv2.resize(enhanced, target_size)
            
            # 4. Rescale pixels to float range [0, 1] or perform standard normalization
            normalized = resized.astype(np.float32) / 255.0
            
            return normalized
            
        except Exception as e:
            self.logger.error(f"Preprocessing failed for {file_path}: {str(e)}")
            # Fallback to standard empty array
            return np.zeros((*target_size, 3), dtype=np.float32)

    def _read_dicom(self, path):
        """Extracts pixel matrices and windowing metadata from DICOM files."""
        if pydicom is None:
            raise ImportError("pydicom library not installed on system. Cannot parse DICOM.")
            
        ds = pydicom.dcmread(str(path))
        pixel_array = ds.pixel_array.astype(np.float32)
        
        # Rescale intercept & slope if present in DICOM tags
        if hasattr(ds, 'RescaleIntercept') and hasattr(ds, 'RescaleSlope'):
            pixel_array = pixel_array * ds.RescaleSlope + ds.RescaleIntercept
            
        # Photometric Interpretation adjustment
        if hasattr(ds, 'PhotometricInterpretation') and ds.PhotometricInterpretation == "MONOCHROME1":
            pixel_array = np.max(pixel_array) - pixel_array
            
        # Normalize between 0 and 255
        p_min, p_max = np.min(pixel_array), np.max(pixel_array)
        if p_max > p_min:
            normalized = ((pixel_array - p_min) / (p_max - p_min)) * 255.0
        else:
            normalized = np.zeros_like(pixel_array)
            
        # Expand grayscale array to 3 channels
        img_3ch = np.stack([normalized] * 3, axis=-1)
        return img_3ch.astype(np.uint8)

    def _read_nifti(self, path):
        """Extracts middle axial slice from NIfTI 3D/4D scans."""
        if nib is None:
            raise ImportError("nibabel library not installed on system. Cannot parse NIfTI.")
            
        img = nib.load(str(path))
        data = img.get_fdata().astype(np.float32)
        
        # Extract mid slice of 3D volume
        if len(data.shape) == 3:
            mid_idx = data.shape[2] // 2
            slice_data = data[:, :, mid_idx]
        elif len(data.shape) == 4:
            mid_idx = data.shape[2] // 2
            slice_data = data[:, :, mid_idx, 0]  # Take first time step
        else:
            slice_data = data
            
        # Normalize to [0, 255]
        s_min, s_max = np.min(slice_data), np.max(slice_data)
        if s_max > s_min:
            normalized = ((slice_data - s_min) / (s_max - s_min)) * 255.0
        else:
            normalized = np.zeros_like(slice_data)
            
        img_3ch = np.stack([normalized] * 3, axis=-1)
        return img_3ch.astype(np.uint8)

    def _read_standard(self, path):
        """Reads PNG, JPG, and BMP files via OpenCV."""
        img = cv2.imread(str(path))
        if img is None:
            # Fallback to PIL
            pil_img = Image.open(str(path))
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            
        # Convert BGR to RGB channel order
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img_rgb

    def _apply_enhancements(self, img, scan_type):
        """Applies clinical adjustments to target organ visibility."""
        scan_type = scan_type.lower()
        
        # Convert standard multi-channel image to single channel grayscale first
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        if scan_type == 'brain':
            # Histogram Equalization for cerebral matter boundaries
            eq_gray = cv2.equalizeHist(gray)
            return np.stack([eq_gray] * 3, axis=-1)
            
        elif scan_type == 'bone':
            # Unsharp masking for fracture line sharpening
            blurred = cv2.GaussianBlur(gray, (0, 0), 2.0)
            enhanced = cv2.addWeighted(gray, 1.5, blurred, -0.5, 0)
            return np.stack([enhanced] * 3, axis=-1)
            
        elif scan_type == 'chest':
            # Morphology closing for lung denoising
            kernel = np.ones((3, 3), np.uint8)
            closed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
            return np.stack([closed] * 3, axis=-1)
            
        elif scan_type == 'cardiac':
            # Contrast Limited Adaptive Histogram Equalization (CLAHE) for ventricle margins
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            cl_gray = clahe.apply(gray)
            # Cardiac U-Net accepts 1-channel or 3-channel; return 3-channel for standard sizing
            return np.stack([cl_gray] * 3, axis=-1)
            
        # Return base image if type not matched
        return img
