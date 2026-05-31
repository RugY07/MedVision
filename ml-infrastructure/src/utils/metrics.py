"""
Metrics and evaluation utilities for medical AI models
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
import seaborn as sns


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Calculate comprehensive metrics for medical classification"""
    
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
        'recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
        'f1_score': f1_score(y_true, y_pred, average='weighted', zero_division=0),
        'precision_macro': precision_score(y_true, y_pred, average='macro', zero_division=0),
        'recall_macro': recall_score(y_true, y_pred, average='macro', zero_division=0),
        'f1_score_macro': f1_score(y_true, y_pred, average='macro', zero_division=0)
    }
    
    return metrics


def calculate_auc_scores(y_true: np.ndarray, y_prob: np.ndarray) -> Dict[str, float]:
    """Calculate AUC scores for multi-class classification"""
    
    try:
        # Macro average AUC
        auc_macro = roc_auc_score(y_true, y_prob, multi_class='ovr', average='macro')
        
        # Micro average AUC
        auc_micro = roc_auc_score(y_true, y_prob, multi_class='ovr', average='micro')
        
        return {
            'auc_macro': auc_macro,
            'auc_micro': auc_micro
        }
    except Exception as e:
        print(f"Error calculating AUC: {e}")
        return {
            'auc_macro': 0.0,
            'auc_micro': 0.0
        }


def plot_confusion_matrix(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    class_names: List[str],
    save_path: str = None,
    figsize: Tuple[int, int] = (10, 8)
):
    """Plot and save confusion matrix"""
    
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=figsize)
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=class_names,
        yticklabels=class_names
    )
    
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_training_history(
    train_losses: List[float],
    val_losses: List[float],
    val_scores: List[float],
    save_path: str = None,
    figsize: Tuple[int, int] = (15, 5)
):
    """Plot training history"""
    
    fig, axes = plt.subplots(1, 3, figsize=figsize)
    
    # Loss plot
    axes[0].plot(train_losses, label='Train Loss')
    axes[0].plot(val_losses, label='Validation Loss')
    axes[0].set_title('Training and Validation Loss')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].legend()
    axes[0].grid(True)
    
    # Score plot
    axes[1].plot(val_scores, label='Validation F1 Score', color='green')
    axes[1].set_title('Validation F1 Score')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('F1 Score')
    axes[1].legend()
    axes[1].grid(True)
    
    # Learning rate plot (if available)
    axes[2].text(0.5, 0.5, 'Learning Rate\n(Not Available)', 
                ha='center', va='center', transform=axes[2].transAxes)
    axes[2].set_title('Learning Rate')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def calculate_medical_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Calculate medical-specific metrics"""
    
    # Basic metrics
    basic_metrics = calculate_metrics(y_true, y_pred)
    
    # Sensitivity (Recall) for each class
    cm = confusion_matrix(y_true, y_pred)
    sensitivities = []
    specificities = []
    
    for i in range(len(cm)):
        # Sensitivity = TP / (TP + FN)
        tp = cm[i, i]
        fn = cm[i, :].sum() - tp
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
        sensitivities.append(sensitivity)
        
        # Specificity = TN / (TN + FP)
        tn = cm.sum() - (cm[i, :].sum() + cm[:, i].sum() - tp)
        fp = cm[:, i].sum() - tp
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        specificities.append(specificity)
    
    medical_metrics = {
        **basic_metrics,
        'mean_sensitivity': np.mean(sensitivities),
        'mean_specificity': np.mean(specificities),
        'min_sensitivity': np.min(sensitivities),
        'min_specificity': np.min(specificities)
    }
    
    return medical_metrics
