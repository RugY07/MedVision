"""
Medical Scan Dataset Classes for Brain, Cardiac, Chest, and Bone Scans
"""

import os
import torch
import numpy as np
import pandas as pd
from PIL import Image
import pydicom
import nibabel as nib
from torch.utils.data import Dataset, DataLoader
from typing import Dict, List, Tuple, Optional, Any
import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2


class MedicalScanDataset(Dataset):
    """Base class for medical scan datasets"""
    
    def __init__(
        self,
        data_dir: str,
        scan_type: str,
        split: str = "train",
        image_size: Tuple[int, int] = (224, 224),
        augmentations: bool = True,
        modalities: List[str] = None
    ):
        self.data_dir = data_dir
        self.scan_type = scan_type
        self.split = split
        self.image_size = image_size
        self.augmentations = augmentations
        self.modalities = modalities or ["default"]
        
        # Load dataset metadata
        self.metadata = self._load_metadata()
        self.classes = self._get_classes()
        self.class_to_idx = {cls: idx for idx, cls in enumerate(self.classes)}
        
        # Setup augmentations
        self.transform = self._setup_transforms()
        
    def _load_metadata(self) -> pd.DataFrame:
        """Load dataset metadata from CSV or directory structure"""
        metadata_path = os.path.join(self.data_dir, f"{self.split}_metadata.csv")
        
        if os.path.exists(metadata_path):
            return pd.read_csv(metadata_path)
        else:
            # Generate metadata from directory structure
            return self._generate_metadata_from_structure()
    
    def _generate_metadata_from_structure(self) -> pd.DataFrame:
        """Generate metadata from directory structure"""
        data = []
        
        for class_name in os.listdir(self.data_dir):
            class_path = os.path.join(self.data_dir, class_name)
            if not os.path.isdir(class_path):
                continue
                
            for filename in os.listdir(class_path):
                if self._is_valid_image_file(filename):
                    data.append({
                        'image_path': os.path.join(class_path, filename),
                        'label': class_name,
                        'scan_type': self.scan_type
                    })
        
        return pd.DataFrame(data)
    
    def _is_valid_image_file(self, filename: str) -> bool:
        """Check if file is a valid medical image"""
        valid_extensions = {'.jpg', '.jpeg', '.png', '.dcm', '.nii', '.nii.gz'}
        return any(filename.lower().endswith(ext) for ext in valid_extensions)
    
    def _get_classes(self) -> List[str]:
        """Get unique classes from metadata"""
        return sorted(self.metadata['label'].unique().tolist())
    
    def _setup_transforms(self):
        """Setup image transformations"""
        if self.split == "train" and self.augmentations:
            return A.Compose([
                A.Resize(self.image_size[0], self.image_size[1]),
                A.RandomRotate90(p=0.5),
                A.Rotate(limit=15, p=0.5),
                A.RandomBrightnessContrast(
                    brightness_limit=0.2,
                    contrast_limit=0.2,
                    p=0.5
                ),
                A.GaussNoise(var_limit=(10.0, 50.0), p=0.3),
                A.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                ),
                ToTensorV2()
            ])
        else:
            return A.Compose([
                A.Resize(self.image_size[0], self.image_size[1]),
                A.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                ),
                ToTensorV2()
            ])
    
    def _load_image(self, image_path: str) -> np.ndarray:
        """Load medical image from various formats"""
        if image_path.endswith('.dcm'):
            return self._load_dicom(image_path)
        elif image_path.endswith(('.nii', '.nii.gz')):
            return self._load_nifti(image_path)
        else:
            return self._load_standard_image(image_path)
    
    def _load_dicom(self, path: str) -> np.ndarray:
        """Load DICOM image"""
        try:
            ds = pydicom.dcmread(path)
            image = ds.pixel_array.astype(np.float32)
            
            # Normalize to 0-255 range
            if image.max() > 255:
                image = (image / image.max()) * 255
            
            # Convert to 3-channel if needed
            if len(image.shape) == 2:
                image = np.stack([image] * 3, axis=-1)
            
            return image.astype(np.uint8)
        except Exception as e:
            print(f"Error loading DICOM {path}: {e}")
            return np.zeros((224, 224, 3), dtype=np.uint8)
    
    def _load_nifti(self, path: str) -> np.ndarray:
        """Load NIfTI image"""
        try:
            img = nib.load(path)
            image = img.get_fdata().astype(np.float32)
            
            # Take middle slice if 3D
            if len(image.shape) == 3:
                image = image[:, :, image.shape[2] // 2]
            
            # Normalize and convert to 3-channel
            image = (image / image.max()) * 255
            image = np.stack([image] * 3, axis=-1)
            
            return image.astype(np.uint8)
        except Exception as e:
            print(f"Error loading NIfTI {path}: {e}")
            return np.zeros((224, 224, 3), dtype=np.uint8)
    
    def _load_standard_image(self, path: str) -> np.ndarray:
        """Load standard image formats (JPEG, PNG)"""
        try:
            image = cv2.imread(path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            return image
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return np.zeros((224, 224, 3), dtype=np.uint8)
    
    def __len__(self) -> int:
        return len(self.metadata)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int, Dict[str, Any]]:
        row = self.metadata.iloc[idx]
        image_path = row['image_path']
        label = row['label']
        
        # Load image
        image = self._load_image(image_path)
        
        # Apply transformations
        transformed = self.transform(image=image)
        image_tensor = transformed['image']
        
        # Get label index
        label_idx = self.class_to_idx[label]
        
        # Additional metadata
        metadata = {
            'image_path': image_path,
            'scan_type': self.scan_type,
            'label': label,
            'split': self.split
        }
        
        return image_tensor, label_idx, metadata


class BrainScanDataset(MedicalScanDataset):
    """Specialized dataset for brain scans"""
    
    def __init__(self, **kwargs):
        super().__init__(
            modalities=["T1", "T2", "FLAIR", "DWI"],
            **kwargs
        )
    
    def _get_classes(self) -> List[str]:
        return ["normal", "tumor", "stroke", "hemorrhage", "atrophy"]


class CardiacScanDataset(MedicalScanDataset):
    """Specialized dataset for cardiac scans"""
    
    def __init__(self, **kwargs):
        super().__init__(
            modalities=["echo", "mri", "ct"],
            **kwargs
        )
    
    def _get_classes(self) -> List[str]:
        return ["normal", "cardiomyopathy", "valvular_disease", "coronary_disease", "arrhythmia"]


class ChestScanDataset(MedicalScanDataset):
    """Specialized dataset for chest scans"""
    
    def __init__(self, **kwargs):
        super().__init__(
            modalities=["xray", "ct"],
            **kwargs
        )
    
    def _get_classes(self) -> List[str]:
        return ["normal", "pneumonia", "covid", "tuberculosis", "lung_cancer", "pneumothorax"]


class BoneScanDataset(MedicalScanDataset):
    """Specialized dataset for bone scans"""
    
    def __init__(self, **kwargs):
        super().__init__(
            modalities=["xray", "mri", "ct"],
            **kwargs
        )
    
    def _get_classes(self) -> List[str]:
        return ["normal", "fracture", "osteoporosis", "arthritis", "tumor"]


def create_data_loaders(
    data_dir: str,
    scan_type: str,
    batch_size: int = 32,
    image_size: Tuple[int, int] = (224, 224),
    num_workers: int = 4
) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """Create data loaders for train, validation, and test sets"""
    
    # Select appropriate dataset class
    dataset_classes = {
        'brain': BrainScanDataset,
        'cardiac': CardiacScanDataset,
        'chest': ChestScanDataset,
        'bone': BoneScanDataset
    }
    
    dataset_class = dataset_classes.get(scan_type, MedicalScanDataset)
    
    # Create datasets
    train_dataset = dataset_class(
        data_dir=data_dir,
        scan_type=scan_type,
        split="train",
        image_size=image_size,
        augmentations=True
    )
    
    val_dataset = dataset_class(
        data_dir=data_dir,
        scan_type=scan_type,
        split="val",
        image_size=image_size,
        augmentations=False
    )
    
    test_dataset = dataset_class(
        data_dir=data_dir,
        scan_type=scan_type,
        split="test",
        image_size=image_size,
        augmentations=False
    )
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    
    return train_loader, val_loader, test_loader
