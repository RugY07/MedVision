"""
Medical AI Model Architectures for Scan Analysis
Specialized models for Brain, Cardiac, Chest, and Bone scans
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
import timm
from typing import Dict, List, Optional, Tuple
import logging


class MedicalScanClassifier(nn.Module):
    """Base classifier for medical scan analysis"""
    
    def __init__(
        self,
        num_classes: int,
        model_name: str = "efficientnet-b4",
        pretrained: bool = True,
        dropout: float = 0.3,
        scan_type: str = "general"
    ):
        super().__init__()
        
        self.num_classes = num_classes
        self.model_name = model_name
        self.scan_type = scan_type
        
        # Load backbone
        if model_name.startswith('efficientnet'):
            self.backbone = timm.create_model(
                model_name, 
                pretrained=pretrained,
                num_classes=0  # Remove final classification layer
            )
            feature_dim = self.backbone.num_features
        else:
            # Use torchvision models
            if model_name == 'resnet50':
                self.backbone = models.resnet50(pretrained=pretrained)
                feature_dim = self.backbone.fc.in_features
                self.backbone = nn.Sequential(*list(self.backbone.children())[:-1])
            elif model_name == 'densenet121':
                self.backbone = models.densenet121(pretrained=pretrained)
                feature_dim = self.backbone.classifier.in_features
                self.backbone = nn.Sequential(*list(self.backbone.children())[:-1])
            else:
                raise ValueError(f"Unsupported model: {model_name}")
        
        # Classification head
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Dropout(dropout),
            nn.Linear(feature_dim, feature_dim // 2),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout),
            nn.Linear(feature_dim // 2, num_classes)
        )
        
        # Attention mechanism for medical images
        self.attention = nn.Sequential(
            nn.Conv2d(feature_dim, feature_dim // 8, 1),
            nn.ReLU(inplace=True),
            nn.Conv2d(feature_dim // 8, 1, 1),
            nn.Sigmoid()
        )
        
    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        # Extract features
        features = self.backbone(x)
        
        # Apply attention
        attention_weights = self.attention(features)
        attended_features = features * attention_weights
        
        # Classification
        logits = self.classifier(attended_features)
        
        return {
            'logits': logits,
            'attention_weights': attention_weights,
            'features': features
        }


class BrainScanModel(MedicalScanClassifier):
    """Specialized model for brain scan analysis"""
    
    def __init__(self, num_classes: int = 5, **kwargs):
        super().__init__(
            num_classes=num_classes,
            model_name=kwargs.get('model_name', 'efficientnet-b4'),
            pretrained=kwargs.get('pretrained', True),
            dropout=kwargs.get('dropout', 0.3),
            scan_type='brain'
        )
        
        # Brain-specific enhancements
        self.region_detector = nn.Sequential(
            nn.Conv2d(self.backbone.num_features, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 128, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 4, 1)  # 4 brain regions
        )
        
    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        base_output = super().forward(x)
        
        # Add region detection
        region_logits = self.region_detector(base_output['features'])
        
        return {
            **base_output,
            'region_logits': region_logits
        }


class CardiacScanModel(MedicalScanClassifier):
    """Specialized model for cardiac scan analysis"""
    
    def __init__(self, num_classes: int = 5, **kwargs):
        super().__init__(
            num_classes=num_classes,
            model_name=kwargs.get('model_name', 'efficientnet-b4'),
            pretrained=kwargs.get('pretrained', True),
            dropout=kwargs.get('dropout', 0.3),
            scan_type='cardiac'
        )
        
        # Cardiac-specific enhancements
        self.chamber_detector = nn.Sequential(
            nn.Conv2d(self.backbone.num_features, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 128, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 4, 1)  # 4 chambers
        )
        
    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        base_output = super().forward(x)
        
        # Add chamber detection
        chamber_logits = self.chamber_detector(base_output['features'])
        
        return {
            **base_output,
            'chamber_logits': chamber_logits
        }


class ChestScanModel(MedicalScanClassifier):
    """Specialized model for chest scan analysis"""
    
    def __init__(self, num_classes: int = 6, **kwargs):
        super().__init__(
            num_classes=num_classes,
            model_name=kwargs.get('model_name', 'efficientnet-b4'),
            pretrained=kwargs.get('pretrained', True),
            dropout=kwargs.get('dropout', 0.3),
            scan_type='chest'
        )
        
        # Chest-specific enhancements
        self.lung_detector = nn.Sequential(
            nn.Conv2d(self.backbone.num_features, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 128, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 2, 1)  # Left and right lung
        )
        
    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        base_output = super().forward(x)
        
        # Add lung detection
        lung_logits = self.lung_detector(base_output['features'])
        
        return {
            **base_output,
            'lung_logits': lung_logits
        }


class BoneScanModel(MedicalScanClassifier):
    """Specialized model for bone scan analysis"""
    
    def __init__(self, num_classes: int = 5, **kwargs):
        super().__init__(
            num_classes=num_classes,
            model_name=kwargs.get('model_name', 'efficientnet-b4'),
            pretrained=kwargs.get('pretrained', True),
            dropout=kwargs.get('dropout', 0.3),
            scan_type='bone'
        )
        
        # Bone-specific enhancements
        self.joint_detector = nn.Sequential(
            nn.Conv2d(self.backbone.num_features, 256, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 128, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 6, 1)  # Major joints
        )
        
    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        base_output = super().forward(x)
        
        # Add joint detection
        joint_logits = self.joint_detector(base_output['features'])
        
        return {
            **base_output,
            'joint_logits': joint_logits
        }


class MultiModalMedicalModel(nn.Module):
    """Multi-modal model that can handle different scan types"""
    
    def __init__(self, scan_types: List[str], num_classes_per_type: Dict[str, int]):
        super().__init__()
        
        self.scan_types = scan_types
        self.num_classes_per_type = num_classes_per_type
        
        # Create specialized models for each scan type
        self.models = nn.ModuleDict({
            'brain': BrainScanModel(num_classes_per_type['brain']),
            'cardiac': CardiacScanModel(num_classes_per_type['cardiac']),
            'chest': ChestScanModel(num_classes_per_type['chest']),
            'bone': BoneScanModel(num_classes_per_type['bone'])
        })
        
        # Shared feature extractor
        self.shared_backbone = timm.create_model('efficientnet-b4', pretrained=True, num_classes=0)
        
    def forward(self, x: torch.Tensor, scan_type: str) -> Dict[str, torch.Tensor]:
        if scan_type not in self.models:
            raise ValueError(f"Unsupported scan type: {scan_type}")
        
        return self.models[scan_type](x)


def create_model(
    scan_type: str,
    num_classes: int,
    model_name: str = "efficientnet-b4",
    pretrained: bool = True,
    **kwargs
) -> MedicalScanClassifier:
    """Factory function to create appropriate model for scan type"""
    
    model_classes = {
        'brain': BrainScanModel,
        'cardiac': CardiacScanModel,
        'chest': ChestScanModel,
        'bone': BoneScanModel
    }
    
    if scan_type not in model_classes:
        raise ValueError(f"Unsupported scan type: {scan_type}")
    
    model_class = model_classes[scan_type]
    
    return model_class(
        num_classes=num_classes,
        model_name=model_name,
        pretrained=pretrained,
        **kwargs
    )


class FocalLoss(nn.Module):
    """Focal Loss for handling class imbalance in medical data"""
    
    def __init__(self, alpha: float = 1.0, gamma: float = 2.0, reduction: str = 'mean'):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction
    
    def forward(self, inputs: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        ce_loss = F.cross_entropy(inputs, targets, reduction='none')
        pt = torch.exp(-ce_loss)
        focal_loss = self.alpha * (1 - pt) ** self.gamma * ce_loss
        
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        else:
            return focal_loss


class MedicalLoss(nn.Module):
    """Combined loss function for medical image analysis"""
    
    def __init__(
        self,
        classification_weight: float = 1.0,
        attention_weight: float = 0.1,
        region_weight: float = 0.1,
        use_focal_loss: bool = True
    ):
        super().__init__()
        
        self.classification_weight = classification_weight
        self.attention_weight = attention_weight
        self.region_weight = region_weight
        
        if use_focal_loss:
            self.classification_loss = FocalLoss()
        else:
            self.classification_loss = nn.CrossEntropyLoss()
        
        self.attention_loss = nn.MSELoss()
        self.region_loss = nn.CrossEntropyLoss()
    
    def forward(
        self,
        outputs: Dict[str, torch.Tensor],
        targets: Dict[str, torch.Tensor]
    ) -> Dict[str, torch.Tensor]:
        losses = {}
        
        # Classification loss
        if 'logits' in outputs and 'labels' in targets:
            losses['classification'] = self.classification_loss(
                outputs['logits'], targets['labels']
            )
        
        # Attention regularization
        if 'attention_weights' in outputs:
            # Encourage attention to be focused
            attention_weights = outputs['attention_weights']
            attention_entropy = -torch.sum(attention_weights * torch.log(attention_weights + 1e-8))
            losses['attention'] = self.attention_weight * attention_entropy
        
        # Region detection loss (if available)
        if 'region_logits' in outputs and 'region_labels' in targets:
            losses['region'] = self.region_weight * self.region_loss(
                outputs['region_logits'], targets['region_labels']
            )
        
        # Total loss
        total_loss = sum(
            losses[key] * getattr(self, f"{key}_weight", 1.0)
            for key in losses
        )
        losses['total'] = total_loss
        
        return losses
