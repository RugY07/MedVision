import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
TRAINING_DIR = BASE_DIR / 'training' / 'brain'
DATASET_DIR = TRAINING_DIR / 'dataset'

TRAIN_DIR = DATASET_DIR / 'train'
VALID_DIR = DATASET_DIR / 'valid'
TEST_DIR = DATASET_DIR / 'test'

# Output directory for exported weights
EXPORT_DIR = BASE_DIR / 'storage' / 'models' / 'brain' / 'v1.0.0'

# Hyperparameters
CLASSES = ['glioma', 'meningioma', 'pituitary', 'notumor']
NUM_CLASSES = len(CLASSES)
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 30
LEARNING_RATE = 1e-4
WEIGHT_DECAY = 1e-5
EARLY_STOPPING_PATIENCE = 7

# Hardware configuration
DEVICE = 'cuda' if os.environ.get('USE_GPU', 'True').lower() == 'true' else 'cpu'

# Create directories if they do not exist
EXPORT_DIR.mkdir(parents=True, exist_ok=True)
TRAIN_DIR.mkdir(parents=True, exist_ok=True)
VALID_DIR.mkdir(parents=True, exist_ok=True)
TEST_DIR.mkdir(parents=True, exist_ok=True)
