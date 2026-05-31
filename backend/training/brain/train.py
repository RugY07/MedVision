import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms, datasets
import logging

# Ensure parent backend directory is in system path for clean imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import config
from app.neural_nets.efficientnet import BrainMRIClassifier

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_dataloaders():
    """Compiles training and validation ImageFolder loaders with augmentations."""
    # Data Augmentations for high variance training
    train_transforms = transforms.Compose([
        transforms.Resize(config.IMG_SIZE),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.1, contrast=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    val_transforms = transforms.Compose([
        transforms.Resize(config.IMG_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Ingest directories, checking for content before binding
    try:
        train_dataset = datasets.ImageFolder(root=str(config.TRAIN_DIR), transform=train_transforms)
        val_dataset = datasets.ImageFolder(root=str(config.VALID_DIR), transform=val_transforms)
        
        train_loader = DataLoader(train_dataset, batch_size=config.BATCH_SIZE, shuffle=True, num_workers=2)
        val_loader = DataLoader(val_dataset, batch_size=config.BATCH_SIZE, shuffle=False, num_workers=2)
        
        logger.info(f"Loaded {len(train_dataset)} training samples across classes: {train_dataset.classes}")
        logger.info(f"Loaded {len(val_dataset)} validation samples.")
        
        return train_loader, val_loader
    except Exception as e:
        logger.warning(
            f"Could not load image folders from disk: {str(e)}. "
            f"Please verify dataset is placed in {config.DATASET_DIR}."
        )
        return None, None

def train_epoch(model, loader, criterion, optimizer, device):
    """Executes single training forward/backward pass epoch."""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for inputs, labels in loader:
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * inputs.size(0)
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

    epoch_loss = running_loss / total
    epoch_acc = (correct / total) * 100
    return epoch_loss, epoch_acc

def validate(model, loader, criterion, device):
    """Executes validation tracking metrics pass."""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            running_loss += loss.item() * inputs.size(0)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

    val_loss = running_loss / total
    val_acc = (correct / total) * 100
    return val_loss, val_acc

def run_training():
    """Main coordinate orchestration for training."""
    device = torch.device(config.DEVICE)
    logger.info(f"Initiating training script on target device: {device}")

    train_loader, val_loader = get_dataloaders()
    if train_loader is None or val_loader is None:
        logger.error("Dataloader initialization failed. Placing dummy mock loop for compilation validation...")
        return

    # Instantiate model using TIMM backbone wrapper
    model = BrainMRIClassifier(num_classes=config.NUM_CLASSES)
    model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=config.LEARNING_RATE, weight_decay=config.WEIGHT_DECAY)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=config.EPOCHS)

    best_val_loss = float('inf')
    early_stop_counter = 0

    for epoch in range(1, config.EPOCHS + 1):
        # 1. Run training loop
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        # 2. Run validation loop
        val_loss, val_acc = validate(model, val_loader, criterion, device)
        
        # Adjust learning rate scheduler
        scheduler.step()

        logger.info(
            f"Epoch [{epoch}/{config.EPOCHS}] - "
            f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}% | "
            f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%"
        )

        # 3. Model Checkpointing & Early Stopping
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            early_stop_counter = 0
            
            # Save checkpoint state dict
            checkpoint_path = config.EXPORT_DIR / 'brain_model.pth'
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_loss': val_loss,
                'val_acc': val_acc
            }, str(checkpoint_path))
            logger.info(f"--> Saved best model checkpoint to {checkpoint_path}")
        else:
            early_stop_counter += 1
            if early_stop_counter >= config.EARLY_STOPPING_PATIENCE:
                logger.info(f"Early stopping triggered after {epoch} epochs of no val loss improvements.")
                break

    logger.info("Training complete.")

if __name__ == '__main__':
    run_training()
