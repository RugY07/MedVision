import torch
import torch.nn as nn

try:
    import timm
except ImportError:
    timm = None

class BaseClassifier(nn.Module):
    """
    Standard classifier block wrapping EfficientNet-B0 backbone using timm
    with a custom global average pooling classifier head.
    """
    def __init__(self, num_classes, model_name='efficientnet_b0', pretrained=False):
        super().__init__()
        self.num_classes = num_classes
        
        if timm is not None:
            # Create feature extractor using timm
            self.backbone = timm.create_model(model_name, pretrained=pretrained, num_classes=0)
            self.in_features = self.backbone.num_features
        else:
            # Fallback CNN structure if timm is absent during local environment build
            self.backbone = nn.Sequential(
                nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1),
                nn.BatchNorm2d(32),
                nn.ReLU(),
                nn.AdaptiveAvgPool2d((1, 1))
            )
            self.in_features = 32
            
        # Classification projection layers
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.3),
            nn.Linear(self.in_features, num_classes)
        )

    def forward(self, x):
        features = self.backbone(x)
        if len(features.shape) > 2:
            features = torch.flatten(features, start_dim=1)
        logits = self.classifier(features)
        return logits


class BrainMRIClassifier(BaseClassifier):
    """
    EfficientNet-B0 classifier tailored for multiclass brain scans diagnostics.
    """
    def __init__(self, num_classes=5, pretrained=False):
        super().__init__(num_classes=num_classes, model_name='efficientnet_b0', pretrained=pretrained)


class BoneFractureClassifier(BaseClassifier):
    """
    EfficientNet-B0 classifier tailored for binary bone fracture diagnostics.
    """
    def __init__(self, num_classes=2, pretrained=False):
        super().__init__(num_classes=num_classes, model_name='efficientnet_b0', pretrained=pretrained)
