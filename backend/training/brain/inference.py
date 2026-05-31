import os
import sys
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import cv2
from PIL import Image
import json
import argparse

# Ensure parent backend directory is in system path for clean imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import config
from app.neural_nets.efficientnet import BrainMRIClassifier

class GradCAM:
    """
    Grad-CAM processor hooks into EfficientNet backbone convolutional feature blocks 
    to map spatial weights and construct diagnostic saliency maps.
    """
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        # Register hooks
        self.target_layer.register_forward_hook(self._save_activation)
        self.target_layer.register_backward_hook(self._save_gradient)

    def _save_activation(self, module, input, output):
        self.activations = output

    def _save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]

    def generate_heatmap(self, input_tensor, class_idx):
        """Calculates Grad-CAM attention heatmap for a specific class index."""
        self.model.zero_grad()
        
        # Forward pass
        output = self.model(input_tensor)
        
        # Target class logit backprop
        loss = output[0, class_idx]
        loss.backward()
        
        # 1. Global average pooling of gradients
        gradients = self.gradients.cpu().data.numpy()[0]
        activations = self.activations.cpu().data.numpy()[0]
        
        weights = np.mean(gradients, axis=(1, 2))
        
        # 2. Weighted combination of activation maps
        cam = np.zeros(activations.shape[1:], dtype=np.float32)
        for i, w in enumerate(weights):
            cam += w * activations[i, :, :]
            
        # 3. Apply ReLU bounding and min-max scale normalization
        cam = np.maximum(cam, 0)
        
        if np.max(cam) > 0:
            cam = cam / np.max(cam)
            
        # Resize to input resolution
        cam = cv2.resize(cam, (input_tensor.shape[2], input_tensor.shape[3]))
        return cam, float(torch.softmax(output, dim=1)[0, class_idx].item())

    def draw_overlay(self, heatmap, original_path, output_path):
        """Blends saliency maps onto original input scan files using OpenCV."""
        img = cv2.imread(original_path)
        if img is None:
            raise FileNotFoundError(f"Original image not found at {original_path}")
            
        h, w = img.shape[:2]
        
        # Convert heatmap to uint8 color bounds
        heatmap_u8 = np.uint8(255 * heatmap)
        heatmap_resized = cv2.resize(heatmap_u8, (w, h))
        
        # Generate pseudo-color mapping
        color_heatmap = cv2.applyColorMap(heatmap_resized, cv2.COLORMAP_JET)
        
        # Combine maps
        alpha = 0.5
        blended = cv2.addWeighted(color_heatmap, alpha, img, 1 - alpha, 0)
        cv2.imwrite(output_path, blended)

def preprocess_image(image_path, target_size=(224, 224)):
    """Loads standard PNG/JPG scan and generates normalized tensor."""
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"File not found: {image_path}")
        
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Simple brain scan equalization
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    eq_gray = cv2.equalizeHist(gray)
    enhanced = np.stack([eq_gray] * 3, axis=-1)
    
    resized = cv2.resize(enhanced, target_size)
    tensor = torch.from_numpy(resized.transpose(2, 0, 1)).float() / 255.0
    
    # Normalize with standard ImageNet params
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    normalized_tensor = normalize(tensor).unsqueeze(0)
    
    return normalized_tensor

def main():
    parser = argparse.ArgumentParser(description="Standalone Local Inference and Grad-CAM Visualizer")
    parser.add_argument("--image", required=True, help="Path to input scan file")
    parser.add_argument("--output", default="storage/results/test_gradcam.png", help="Path to save result heatmap")
    args = parser.parse_args()

    # Hardware check
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Executing inference utility on device: {device}")

    # Load model and config
    model_path = config.EXPORT_DIR / 'brain_model.pth'
    if not os.path.exists(model_path):
        print(f"Exported model weights not found at {model_path}. Please complete export.py dry-run or train.py first.")
        sys.exit(1)

    model = BrainMRIClassifier(num_classes=config.NUM_CLASSES)
    
    # Try loading state dict
    try:
        state_dict = torch.load(model_path, map_location=device)
        model.load_state_dict(state_dict)
    except Exception:
        # Fallback if checkpoint contains complex dictionary (e.g. before export.py)
        checkpoint = torch.load(model_path, map_location=device)
        model.load_state_dict(checkpoint.get('model_state_dict', checkpoint))

    model.to(device)
    model.eval()

    # Build input tensor
    try:
        input_tensor = preprocess_image(args.image)
        input_tensor = input_tensor.to(device)
    except Exception as e:
        print(f"Preprocessing error: {str(e)}")
        sys.exit(1)

    # Instantiate Grad-CAM engine hooking target layer
    target_layer = model.backbone.conv_head if hasattr(model.backbone, 'conv_head') else model.backbone[-1]
    cam_engine = GradCAM(model, target_layer)

    # Forward prediction run
    outputs = model(input_tensor)
    _, predicted_idx = outputs.max(1)
    predicted_idx = int(predicted_idx.item())
    
    predicted_class = config.CLASSES[predicted_idx]

    # Generate heatmaps
    heatmap, confidence = cam_engine.generate_heatmap(input_tensor, predicted_idx)

    # Export output image overlay
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    cam_engine.draw_overlay(heatmap, args.image, args.output)

    print("="*60)
    print("                MedVision-AI Local Diagnostic Result")
    print("="*60)
    print(f"Class Prediction:  {predicted_class.upper()}")
    print(f"Model Confidence:  {confidence * 100:.2f}%")
    print(f"Output CAM Saved:  {args.output}")
    print("="*60)

if __name__ == '__main__':
    # Add simple check to allow executing import checks easily
    if len(sys.argv) > 1:
        main()
    else:
        print("Standalone inference utility loaded successfully.")
