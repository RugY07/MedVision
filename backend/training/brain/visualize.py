import os
import sys
import numpy as np

# Try importing plotting tools, manage import failures for standalone executions
try:
    import matplotlib
    matplotlib.use('Agg') # Safe headless plotting
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError:
    plt = None
    sns = None

# Ensure parent backend directory is in system path for clean imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

def plot_training_metrics(train_losses, val_losses, train_accs, val_accs, output_dir=None):
    """Generates and saves dual-axis line charts showing training/validation convergence."""
    if plt is None:
        print("Matplotlib not installed. Visual curves plotting skipped.")
        return

    output_dir = output_dir or config.EXPORT_DIR
    epochs = range(1, len(train_losses) + 1)

    # 1. Plot Loss curves
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(epochs, train_losses, 'b-', label='Training Loss')
    plt.plot(epochs, val_losses, 'r-', label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.grid(True)
    plt.legend()

    # 2. Plot Accuracy curves
    plt.subplot(1, 2, 2)
    plt.plot(epochs, train_accs, 'b-', label='Training Accuracy')
    plt.plot(epochs, val_accs, 'r-', label='Validation Accuracy')
    plt.title('Training and Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy (%)')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    loss_curve_path = os.path.join(output_dir, 'training_curves.png')
    plt.savefig(loss_curve_path, dpi=300)
    plt.close()
    print(f"Convergence curves plotted successfully to {loss_curve_path}")

def plot_confusion_matrix(matrix, class_names, output_dir=None):
    """Draws and exports heatmaps for confusion matrix metrics."""
    if plt is None or sns is None:
        print("Seaborn/Matplotlib not installed. Confusion matrix visualization skipped.")
        return

    output_dir = output_dir or config.EXPORT_DIR
    plt.figure(figsize=(8, 6))
    
    sns.heatmap(
        matrix, 
        annot=True, 
        fmt='d', 
        cmap='Blues', 
        xticklabels=[c.upper() for c in class_names],
        yticklabels=[c.upper() for c in class_names]
    )
    
    plt.title('Brain MRI Classifier Confusion Matrix')
    plt.ylabel('Ground Truth Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    
    matrix_path = os.path.join(output_dir, 'confusion_matrix.png')
    plt.savefig(matrix_path, dpi=300)
    plt.close()
    print(f"Confusion matrix heatmap plotted successfully to {matrix_path}")

if __name__ == '__main__':
    # Standalone mock run to verify visualization tools compilation
    mock_train_loss = [0.9, 0.7, 0.5, 0.4, 0.3]
    mock_val_loss = [0.8, 0.6, 0.55, 0.45, 0.42]
    mock_train_acc = [65.0, 75.0, 82.0, 86.0, 89.0]
    mock_val_acc = [68.0, 76.0, 80.0, 84.0, 85.0]
    
    mock_matrix = np.array([
        [45, 2, 1, 2],
        [3, 40, 4, 3],
        [1, 2, 47, 0],
        [2, 3, 1, 44]
    ])
    
    print("Running visualizer self-test...")
    plot_training_metrics(mock_train_loss, mock_val_loss, mock_train_acc, mock_val_acc)
    plot_confusion_matrix(mock_matrix, config.CLASSES)
