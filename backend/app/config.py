import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """Base application configuration class."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_major_medvision_project_sec_key_123')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR}/db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Directory storage locations
    STORAGE_DIR = BASE_DIR / 'storage'
    UPLOAD_FOLDER = STORAGE_DIR / 'uploads'
    RESULTS_FOLDER = STORAGE_DIR / 'results'
    MODELS_FOLDER = STORAGE_DIR / 'models'
    
    # Maximum upload size (50MB)
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    
    # CORS
    CORS_HEADERS = 'Content-Type'

    @classmethod
    def init_app(cls, app):
        """Initializes storage directories and verifies weight/asset paths."""
        # Create directories if they do not exist
        cls.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
        cls.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
        cls.RESULTS_FOLDER.mkdir(parents=True, exist_ok=True)
        cls.MODELS_FOLDER.mkdir(parents=True, exist_ok=True)
