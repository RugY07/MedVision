import torch
import torch.nn as nn

try:
    import timm
except ImportError:
    timm = None

class ChestXRayClassifier(nn.Module):
    """
    CheXNet-inspired DenseNet-121 model designed for multi-label binary
    pulmonary pathology classifications.
    """
    def __init__(self, num_classes=6, pretrained=False):
        super().__init__()
        self.num_classes = num_classes
        
        if timm is not None:
            # Create feature extractor using densenet121 from timm
            self.backbone = timm.create_model('densenet121', pretrained=pretrained, num_classes=0)
            self.in_features = self.backbone.num_features
        else:
            # Fallback simple CNN blocks
            self.backbone = nn.Sequential(
                nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3),
                nn.BatchNorm2d(64),
                nn.ReLU(),
                nn.AdaptiveAvgPool2d((1, 1))
            )
            self.in_features = 64

        # Multi-label classification head
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.2),
            nn.Linear(self.in_features, num_classes)
        )

    def forward(self, x):
        features = self.backbone(x)
        if len(features.shape) > 2:
            features = torch.flatten(features, start_dim=1)
        logits = self.classifier(features)
        return logits
