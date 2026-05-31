import os
import sys
import torch
from torch.utils.data import DataLoader
from torchvision import transforms, datasets
import logging
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support
import numpy as np

# Ensure parent backend directory is in system path for clean imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import config
from app.neural_nets.efficientnet import BrainMRIClassifier

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def evaluate_model():
    """Ingests test dataset, runs validation metrics pass, and saves report."""
    device = torch.device(config.DEVICE)
    logger.info(f"Running model evaluation pipeline on device: {device}")

    # 1. Dataset loading with standard test transforms
    test_transforms = transforms.Compose([
        transforms.Resize(config.IMG_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    try:
        test_dataset = datasets.ImageFolder(root=str(config.TEST_DIR), transform=test_transforms)
        test_loader = DataLoader(test_dataset, batch_size=config.BATCH_SIZE, shuffle=False, num_workers=2)
    except Exception as e:
        logger.error(f"Failed to load test dataset from {config.TEST_DIR}: {str(e)}")
        return

    # 2. Reconstruct model architecture and load best checkpoint
    model_path = config.EXPORT_DIR / 'brain_model.pth'
    if not os.path.exists(model_path):
        logger.error(f"Trained weight checkpoint not found at {model_path}. Run train.py first.")
        return

    model = BrainMRIClassifier(num_classes=config.NUM_CLASSES)
    try:
        checkpoint = torch.load(model_path, map_location=device)
        model.load_state_dict(checkpoint['model_state_dict'])
        logger.info(f"Loaded checkpoint from epoch {checkpoint.get('epoch', 'unknown')} with validation loss: {checkpoint.get('val_loss', 'N/A')}")
    except Exception as e:
        logger.error(f"Error loading model weights: {str(e)}")
        return

    model.to(device)
    model.eval()

    # 3. Validation Inference Loop
    y_true = []
    y_pred = []

    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            
            y_true.extend(labels.numpy())
            y_pred.extend(predicted.cpu().numpy())

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    # 4. Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='macro')
    
    matrix = confusion_matrix(y_true, y_pred)
    class_report = classification_report(y_true, y_pred, target_names=config.CLASSES)

    # 5. Compile and export report to local storage
    report_path = config.EXPORT_DIR / 'evaluation_report.txt'
    with open(report_path, 'w') as f:
        f.write("="*60 + "\n")
        f.write("      MedVision-AI Brain MRI Classifier Evaluation Report\n")
        f.write("="*60 + "\n\n")
        f.write(f"Model Identifier: EfficientNet-B0 Brain Classifier (v1.0.0)\n")
        f.write(f"Dataset Split: Test set from {config.TEST_DIR}\n")
        f.write(f"Evaluation Time: {np.datetime64('now')}\n\n")
        f.write(f"Overall Metrics:\n")
        f.write(f"  - Accuracy:  {accuracy * 100:.2f}%\n")
        f.write(f"  - Precision: {precision * 100:.2f}%\n")
        f.write(f"  - Recall:    {recall * 100:.2f}%\n")
        f.write(f"  - F1 Score:  {f1 * 100:.2f}%\n\n")
        f.write("Classification Report:\n")
        f.write(class_report + "\n")
        f.write("Confusion Matrix:\n")
        f.write(str(matrix) + "\n\n")
        f.write("Legend Classes:\n")
        for i, cls in enumerate(config.CLASSES):
            f.write(f"  Index {i} -> {cls.upper()}\n")

    logger.info(f"Evaluation report compiled and written to: {report_path}")
    logger.info(f"Accuracy: {accuracy * 100:.2f}% | F1 Score: {f1 * 100:.2f}%")

if __name__ == '__main__':
    evaluate_model()
