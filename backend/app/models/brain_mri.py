import torch
import torch.nn as nn
import numpy as np
import cv2

try:
    import timm
except ImportError:
    timm = None

class BrainMRIClassifier(nn.Module):
    """
    EfficientNet-B0 network structure optimized for multiclass Brain MRI classification.
    Includes forward/backward hooks to calculate Grad-CAM heatmaps at runtime.
    """
    def __init__(self, num_classes=4, pretrained=False):
        super().__init__()
        self.num_classes = num_classes
        
        if timm is not None:
            # Create feature extractor using timm
            self.backbone = timm.create_model('efficientnet_b0', pretrained=pretrained, num_classes=0)
            self.in_features = self.backbone.num_features
        else:
            # Fallback simple CNN blocks if timm is absent
            self.backbone = nn.Sequential(
                nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1),
                nn.BatchNorm2d(32),
                nn.ReLU(),
                nn.AdaptiveAvgPool2d((1, 1))
            )
            self.in_features = 32

        # Classification Projection Head
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.3),
            nn.Linear(self.in_features, num_classes)
        )
        
        # Saliency hooks properties
        self.gradients = None
        self.activations = None
        self._register_saliency_hooks()

    def _register_saliency_hooks(self):
        """Registers hooks on the final convolutional layer of the backbone."""
        # In EfficientNet-B0, conv_head is the last conv layer before pooling
        if timm is not None and hasattr(self.backbone, 'conv_head'):
            target_layer = self.backbone.conv_head
        else:
            # Fallback target layer
            target_layer = self.backbone[-1]

        target_layer.register_forward_hook(self._save_activation)
        target_layer.register_backward_hook(self._save_gradient)

    def _save_activation(self, module, input, output):
        self.activations = output

    def _save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]

    def forward(self, x):
        features = self.backbone(x)
        if len(features.shape) > 2:
            features = torch.flatten(features, start_dim=1)
        logits = self.classifier(features)
        return logits

    def generate_gradcam_overlay(self, input_tensor, class_idx, raw_image_path, output_image_path):
        """
        Backpropagates logit activations for target classes to capture 
        saliency gradients and overlays pseudo-color heatmaps using OpenCV.
        """
        self.zero_grad()
        
        # Forward pass
        logits = self(input_tensor)
        
        # Target class backprop
        score = logits[0, class_idx]
        score.backward()
        
        # Extract features and average spatial gradients
        gradients = self.gradients.cpu().data.numpy()[0]
        activations = self.activations.cpu().data.numpy()[0]
        
        weights = np.mean(gradients, axis=(1, 2))
        
        # Weighted activation maps linear combination
        cam = np.zeros(activations.shape[1:], dtype=np.float32)
        for i, w in enumerate(weights):
            cam += w * activations[i, :, :]
            
        # Apply ReLU activation and normalize bounds
        cam = np.maximum(cam, 0)
        if np.max(cam) > 0:
            cam = cam / np.max(cam)
            
        # Read raw image
        raw_img = cv2.imread(raw_image_path)
        if raw_img is None:
            raw_img = np.zeros((224, 224, 3), dtype=np.uint8)
            
        h, w = raw_img.shape[:2]
        
        # Resize saliency heatmap to match original scan dimensions
        cam_u8 = np.uint8(255 * cam)
        cam_resized = cv2.resize(cam_u8, (w, h))
        
        # Create Jet Color Map overlay
        color_heatmap = cv2.applyColorMap(cam_resized, cv2.COLORMAP_JET)
        
        # Blend overlay onto raw image
        alpha = 0.5
        blended = cv2.addWeighted(color_heatmap, alpha, raw_img, 1 - alpha, 0)
        
        # Export file output
        cv2.imwrite(output_image_path, blended)
        
        pred_label = torch.argmax(logits, dim=1).item()
        confidence = torch.softmax(logits, dim=1)[0, class_idx].item()
        
        return confidence
