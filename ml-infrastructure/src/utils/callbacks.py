"""
Training callbacks for medical AI models
"""

import os
import torch
import numpy as np
from typing import Dict, Any, Optional


class EarlyStopping:
    """Early stopping callback to prevent overfitting"""
    
    def __init__(
        self,
        patience: int = 10,
        min_delta: float = 0.001,
        restore_best_weights: bool = True
    ):
        self.patience = patience
        self.min_delta = min_delta
        self.restore_best_weights = restore_best_weights
        
        self.wait = 0
        self.stopped_epoch = 0
        self.best_score = None
        self.best_weights = None
        
    def __call__(self, val_score: float, model: torch.nn.Module = None) -> bool:
        """
        Check if training should stop early
        
        Args:
            val_score: Current validation score
            model: Model to save best weights from
            
        Returns:
            True if training should stop, False otherwise
        """
        if self.best_score is None:
            self.best_score = val_score
            if model is not None:
                self.best_weights = model.state_dict().copy()
        elif val_score < self.best_score + self.min_delta:
            self.wait += 1
            if self.wait >= self.patience:
                self.stopped_epoch = self.wait
                if self.restore_best_weights and self.best_weights is not None:
                    model.load_state_dict(self.best_weights)
                return True
        else:
            self.best_score = val_score
            self.wait = 0
            if model is not None:
                self.best_weights = model.state_dict().copy()
        
        return False


class ModelCheckpoint:
    """Model checkpoint callback to save best models"""
    
    def __init__(
        self,
        save_dir: str,
        filename: str = 'best_model.pth',
        monitor: str = 'f1_score',
        mode: str = 'max',
        save_best_only: bool = True,
        save_last: bool = True
    ):
        self.save_dir = save_dir
        self.filename = filename
        self.monitor = monitor
        self.mode = mode
        self.save_best_only = save_best_only
        self.save_last = save_last
        
        self.best_score = None
        self.last_epoch = 0
        
        # Create save directory
        os.makedirs(save_dir, exist_ok=True)
    
    def __call__(
        self,
        metrics: Dict[str, float],
        model: torch.nn.Module,
        optimizer: torch.optim.Optimizer,
        epoch: int,
        additional_info: Dict[str, Any] = None
    ):
        """
        Save model checkpoint based on metrics
        
        Args:
            metrics: Current validation metrics
            model: Model to save
            optimizer: Optimizer state
            epoch: Current epoch
            additional_info: Additional information to save
        """
        current_score = metrics.get(self.monitor)
        
        if current_score is None:
            print(f"Warning: Monitor metric '{self.monitor}' not found in metrics")
            return
        
        # Determine if this is the best score
        is_best = False
        if self.best_score is None:
            is_best = True
            self.best_score = current_score
        elif self.mode == 'max' and current_score > self.best_score:
            is_best = True
            self.best_score = current_score
        elif self.mode == 'min' and current_score < self.best_score:
            is_best = True
            self.best_score = current_score
        
        # Save checkpoint
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'metrics': metrics,
            'best_score': self.best_score
        }
        
        if additional_info:
            checkpoint.update(additional_info)
        
        # Save best model
        if is_best and self.save_best_only:
            best_path = os.path.join(self.save_dir, self.filename)
            torch.save(checkpoint, best_path)
            print(f"New best model saved: {best_path} (Score: {current_score:.4f})")
        
        # Save last model
        if self.save_last:
            last_path = os.path.join(self.save_dir, 'last_model.pth')
            torch.save(checkpoint, last_path)
        
        self.last_epoch = epoch


class LearningRateScheduler:
    """Custom learning rate scheduler"""
    
    def __init__(
        self,
        optimizer: torch.optim.Optimizer,
        mode: str = 'min',
        factor: float = 0.5,
        patience: int = 5,
        min_lr: float = 1e-7
    ):
        self.optimizer = optimizer
        self.mode = mode
        self.factor = factor
        self.patience = patience
        self.min_lr = min_lr
        
        self.wait = 0
        self.best_score = None
        
    def __call__(self, val_score: float):
        """Update learning rate based on validation score"""
        if self.best_score is None:
            self.best_score = val_score
        elif self.mode == 'min' and val_score < self.best_score - 1e-4:
            self.best_score = val_score
            self.wait = 0
        elif self.mode == 'max' and val_score > self.best_score + 1e-4:
            self.best_score = val_score
            self.wait = 0
        else:
            self.wait += 1
            
            if self.wait >= self.patience:
                self._reduce_lr()
                self.wait = 0
    
    def _reduce_lr(self):
        """Reduce learning rate"""
        for param_group in self.optimizer.param_groups:
            old_lr = param_group['lr']
            new_lr = max(old_lr * self.factor, self.min_lr)
            param_group['lr'] = new_lr
            print(f"Reducing learning rate from {old_lr:.6f} to {new_lr:.6f}")


class MetricsLogger:
    """Callback to log training metrics"""
    
    def __init__(self, log_file: str = None):
        self.log_file = log_file
        self.metrics_history = []
        
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    def __call__(self, epoch: int, metrics: Dict[str, float]):
        """Log metrics for current epoch"""
        log_entry = {
            'epoch': epoch,
            **metrics
        }
        
        self.metrics_history.append(log_entry)
        
        # Print to console
        metrics_str = ', '.join([f"{k}: {v:.4f}" for k, v in metrics.items()])
        print(f"Epoch {epoch}: {metrics_str}")
        
        # Save to file
        if self.log_file:
            with open(self.log_file, 'a') as f:
                f.write(f"{epoch},{','.join([str(v) for v in metrics.values()])}\n")
    
    def get_best_epoch(self, metric: str, mode: str = 'max') -> int:
        """Get epoch with best metric value"""
        if not self.metrics_history:
            return 0
        
        best_epoch = 0
        best_value = self.metrics_history[0].get(metric, 0)
        
        for entry in self.metrics_history[1:]:
            value = entry.get(metric, 0)
            
            if mode == 'max' and value > best_value:
                best_value = value
                best_epoch = entry['epoch']
            elif mode == 'min' and value < best_value:
                best_value = value
                best_epoch = entry['epoch']
        
        return best_epoch


class GradientClipping:
    """Gradient clipping callback"""
    
    def __init__(self, max_norm: float = 1.0):
        self.max_norm = max_norm
    
    def __call__(self, model: torch.nn.Module):
        """Apply gradient clipping"""
        torch.nn.utils.clip_grad_norm_(model.parameters(), self.max_norm)
