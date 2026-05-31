"""
Medical AI Model Training Script
Handles training for Brain, Cardiac, Chest, and Bone scan models
"""

import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
import logging
from pathlib import Path
import wandb
import mlflow
from tqdm import tqdm
import json
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

from ..data.dataset import create_data_loaders
from ..models.medical_models import create_model, MedicalLoss, FocalLoss
from ..utils.metrics import calculate_metrics, plot_confusion_matrix
from ..utils.callbacks import EarlyStopping, ModelCheckpoint


class MedicalModelTrainer:
    """Trainer class for medical scan models"""
    
    def __init__(
        self,
        scan_type: str,
        config: Dict[str, Any],
        device: str = "cuda"
    ):
        self.scan_type = scan_type
        self.config = config
        self.device = device
        
        # Setup logging
        self.logger = logging.getLogger(f"trainer_{scan_type}")
        self.logger.setLevel(logging.INFO)
        
        # Initialize tracking
        self.setup_tracking()
        
        # Training state
        self.current_epoch = 0
        self.best_val_score = 0.0
        self.train_losses = []
        self.val_losses = []
        self.val_scores = []
        
    def setup_tracking(self):
        """Setup experiment tracking"""
        if self.config.get('wandb', {}).get('enabled', False):
            wandb.init(
                project=self.config['wandb']['project'],
                name=f"{self.scan_type}_scan_model",
                config=self.config
            )
        
        if self.config.get('mlflow', {}).get('enabled', False):
            mlflow.set_tracking_uri(self.config['mlflow']['tracking_uri'])
            mlflow.set_experiment(f"{self.scan_type}_medical_scan")
    
    def prepare_data(self) -> Tuple[DataLoader, DataLoader, DataLoader]:
        """Prepare data loaders"""
        self.logger.info(f"Preparing data for {self.scan_type} scans...")
        
        data_config = self.config['datasets'][self.scan_type]
        
        train_loader, val_loader, test_loader = create_data_loaders(
            data_dir=data_config['path'],
            scan_type=self.scan_type,
            batch_size=self.config['training']['batch_size'],
            image_size=data_config['image_size'],
            num_workers=self.config['hardware']['num_workers']
        )
        
        self.logger.info(f"Data prepared: Train={len(train_loader)}, Val={len(val_loader)}, Test={len(test_loader)}")
        
        return train_loader, val_loader, test_loader
    
    def create_model(self) -> nn.Module:
        """Create model for the specific scan type"""
        self.logger.info(f"Creating {self.scan_type} model...")
        
        data_config = self.config['datasets'][self.scan_type]
        model_config = self.config['models']
        
        model = create_model(
            scan_type=self.scan_type,
            num_classes=len(data_config['classes']),
            model_name=model_config['architecture'],
            pretrained=model_config['pretrained'],
            dropout=model_config['dropout']
        )
        
        model = model.to(self.device)
        
        # Log model info
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        
        self.logger.info(f"Model created: {total_params:,} total params, {trainable_params:,} trainable")
        
        return model
    
    def create_optimizer_and_scheduler(self, model: nn.Module) -> Tuple[optim.Optimizer, Any]:
        """Create optimizer and learning rate scheduler"""
        training_config = self.config['training']
        
        # Optimizer
        if training_config.get('optimizer', 'adam') == 'adam':
            optimizer = optim.Adam(
                model.parameters(),
                lr=training_config['learning_rate'],
                weight_decay=training_config.get('weight_decay', 1e-4)
            )
        elif training_config['optimizer'] == 'adamw':
            optimizer = optim.AdamW(
                model.parameters(),
                lr=training_config['learning_rate'],
                weight_decay=training_config.get('weight_decay', 1e-4)
            )
        else:
            optimizer = optim.SGD(
                model.parameters(),
                lr=training_config['learning_rate'],
                momentum=0.9,
                weight_decay=training_config.get('weight_decay', 1e-4)
            )
        
        # Scheduler
        if training_config.get('scheduler') == 'cosine':
            scheduler = optim.lr_scheduler.CosineAnnealingLR(
                optimizer,
                T_max=training_config['epochs']
            )
        elif training_config.get('scheduler') == 'plateau':
            scheduler = optim.lr_scheduler.ReduceLROnPlateau(
                optimizer,
                mode='max',
                factor=0.5,
                patience=5,
                verbose=True
            )
        else:
            scheduler = None
        
        return optimizer, scheduler
    
    def create_loss_function(self) -> nn.Module:
        """Create loss function"""
        training_config = self.config['training']
        
        if training_config.get('use_focal_loss', True):
            loss_fn = MedicalLoss(
                use_focal_loss=True,
                classification_weight=training_config.get('classification_weight', 1.0),
                attention_weight=training_config.get('attention_weight', 0.1),
                region_weight=training_config.get('region_weight', 0.1)
            )
        else:
            loss_fn = nn.CrossEntropyLoss()
        
        return loss_fn
    
    def train_epoch(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        optimizer: optim.Optimizer,
        loss_fn: nn.Module
    ) -> Dict[str, float]:
        """Train for one epoch"""
        model.train()
        
        total_loss = 0.0
        correct = 0
        total = 0
        
        progress_bar = tqdm(train_loader, desc=f"Epoch {self.current_epoch}")
        
        for batch_idx, (images, labels, metadata) in enumerate(progress_bar):
            images, labels = images.to(self.device), labels.to(self.device)
            
            optimizer.zero_grad()
            
            # Forward pass
            outputs = model(images)
            
            # Calculate loss
            if isinstance(outputs, dict):
                targets = {'labels': labels}
                losses = loss_fn(outputs, targets)
                loss = losses['total']
            else:
                loss = loss_fn(outputs, labels)
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            # Statistics
            total_loss += loss.item()
            if isinstance(outputs, dict):
                _, predicted = outputs['logits'].max(1)
            else:
                _, predicted = outputs.max(1)
            
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
            # Update progress bar
            progress_bar.set_postfix({
                'Loss': f'{loss.item():.4f}',
                'Acc': f'{100.*correct/total:.2f}%'
            })
        
        epoch_loss = total_loss / len(train_loader)
        epoch_acc = 100. * correct / total
        
        return {
            'loss': epoch_loss,
            'accuracy': epoch_acc
        }
    
    def validate_epoch(
        self,
        model: nn.Module,
        val_loader: DataLoader,
        loss_fn: nn.Module
    ) -> Dict[str, float]:
        """Validate for one epoch"""
        model.eval()
        
        total_loss = 0.0
        all_predictions = []
        all_labels = []
        
        with torch.no_grad():
            for images, labels, metadata in val_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                
                # Forward pass
                outputs = model(images)
                
                # Calculate loss
                if isinstance(outputs, dict):
                    targets = {'labels': labels}
                    losses = loss_fn(outputs, targets)
                    loss = losses['total']
                    predictions = outputs['logits'].argmax(1)
                else:
                    loss = loss_fn(outputs, labels)
                    predictions = outputs.argmax(1)
                
                total_loss += loss.item()
                
                all_predictions.extend(predictions.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
        
        # Calculate metrics
        metrics = calculate_metrics(all_labels, all_predictions)
        metrics['loss'] = total_loss / len(val_loader)
        
        return metrics
    
    def train(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        optimizer: optim.Optimizer,
        scheduler: Any,
        loss_fn: nn.Module,
        save_dir: str
    ):
        """Main training loop"""
        self.logger.info(f"Starting training for {self.scan_type} model...")
        
        # Setup callbacks
        early_stopping = EarlyStopping(
            patience=self.config['training'].get('patience', 15),
            min_delta=0.001
        )
        
        model_checkpoint = ModelCheckpoint(
            save_dir=save_dir,
            filename=f'{self.scan_type}_best_model.pth',
            monitor='f1_score',
            mode='max'
        )
        
        for epoch in range(self.config['training']['epochs']):
            self.current_epoch = epoch
            
            # Training
            train_metrics = self.train_epoch(model, train_loader, optimizer, loss_fn)
            
            # Validation
            val_metrics = self.validate_epoch(model, val_loader, loss_fn)
            
            # Update scheduler
            if scheduler is not None:
                if isinstance(scheduler, optim.lr_scheduler.ReduceLROnPlateau):
                    scheduler.step(val_metrics['f1_score'])
                else:
                    scheduler.step()
            
            # Log metrics
            self.log_metrics(epoch, train_metrics, val_metrics)
            
            # Save training state
            self.train_losses.append(train_metrics['loss'])
            self.val_losses.append(val_metrics['loss'])
            self.val_scores.append(val_metrics['f1_score'])
            
            # Model checkpoint
            model_checkpoint(val_metrics, model, optimizer, epoch)
            
            # Early stopping
            if early_stopping(val_metrics['f1_score']):
                self.logger.info(f"Early stopping at epoch {epoch}")
                break
        
        self.logger.info("Training completed!")
    
    def log_metrics(self, epoch: int, train_metrics: Dict, val_metrics: Dict):
        """Log training metrics"""
        # Console logging
        self.logger.info(
            f"Epoch {epoch}: "
            f"Train Loss: {train_metrics['loss']:.4f}, "
            f"Train Acc: {train_metrics['accuracy']:.2f}%, "
            f"Val Loss: {val_metrics['loss']:.4f}, "
            f"Val F1: {val_metrics['f1_score']:.4f}"
        )
        
        # Wandb logging
        if self.config.get('wandb', {}).get('enabled', False):
            wandb.log({
                'epoch': epoch,
                'train/loss': train_metrics['loss'],
                'train/accuracy': train_metrics['accuracy'],
                'val/loss': val_metrics['loss'],
                'val/f1_score': val_metrics['f1_score'],
                'val/precision': val_metrics['precision'],
                'val/recall': val_metrics['recall'],
                'learning_rate': optimizer.param_groups[0]['lr']
            })
        
        # MLflow logging
        if self.config.get('mlflow', {}).get('enabled', False):
            with mlflow.start_run():
                mlflow.log_metrics({
                    'train_loss': train_metrics['loss'],
                    'train_accuracy': train_metrics['accuracy'],
                    'val_loss': val_metrics['loss'],
                    'val_f1_score': val_metrics['f1_score']
                }, step=epoch)
    
    def evaluate_model(
        self,
        model: nn.Module,
        test_loader: DataLoader,
        save_dir: str
    ) -> Dict[str, float]:
        """Evaluate model on test set"""
        self.logger.info("Evaluating model on test set...")
        
        model.eval()
        all_predictions = []
        all_labels = []
        all_probabilities = []
        
        with torch.no_grad():
            for images, labels, metadata in test_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                
                outputs = model(images)
                
                if isinstance(outputs, dict):
                    logits = outputs['logits']
                else:
                    logits = outputs
                
                probabilities = F.softmax(logits, dim=1)
                predictions = logits.argmax(1)
                
                all_predictions.extend(predictions.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
                all_probabilities.extend(probabilities.cpu().numpy())
        
        # Calculate metrics
        metrics = calculate_metrics(all_labels, all_predictions)
        
        # Generate classification report
        data_config = self.config['datasets'][self.scan_type]
        class_names = data_config['classes']
        
        report = classification_report(
            all_labels, all_predictions,
            target_names=class_names,
            output_dict=True
        )
        
        # Plot confusion matrix
        plot_confusion_matrix(
            all_labels, all_predictions,
            class_names=class_names,
            save_path=os.path.join(save_dir, f'{self.scan_type}_confusion_matrix.png')
        )
        
        # Save results
        results = {
            'metrics': metrics,
            'classification_report': report,
            'predictions': all_predictions,
            'labels': all_labels,
            'probabilities': all_probabilities
        }
        
        with open(os.path.join(save_dir, f'{self.scan_type}_test_results.json'), 'w') as f:
            json.dump(results, f, indent=2)
        
        self.logger.info(f"Test Results: {metrics}")
        
        return metrics


def train_medical_model(
    scan_type: str,
    config: Dict[str, Any],
    save_dir: str
) -> Dict[str, Any]:
    """Main training function"""
    
    # Create save directory
    os.makedirs(save_dir, exist_ok=True)
    
    # Setup device
    device = torch.device(config['hardware']['device'] if torch.cuda.is_available() else 'cpu')
    
    # Initialize trainer
    trainer = MedicalModelTrainer(scan_type, config, device)
    
    # Prepare data
    train_loader, val_loader, test_loader = trainer.prepare_data()
    
    # Create model
    model = trainer.create_model()
    
    # Create optimizer and scheduler
    optimizer, scheduler = trainer.create_optimizer_and_scheduler(model)
    
    # Create loss function
    loss_fn = trainer.create_loss_function()
    
    # Train model
    trainer.train(model, train_loader, val_loader, optimizer, scheduler, loss_fn, save_dir)
    
    # Load best model
    best_model_path = os.path.join(save_dir, f'{scan_type}_best_model.pth')
    if os.path.exists(best_model_path):
        model.load_state_dict(torch.load(best_model_path))
    
    # Evaluate on test set
    test_metrics = trainer.evaluate_model(model, test_loader, save_dir)
    
    return {
        'model': model,
        'test_metrics': test_metrics,
        'config': config
    }
