import os
import logging
from flask import Flask
from dotenv import load_dotenv

# Load environmental configs from .env
load_dotenv()

from .config import Config
from .extensions import db, cors, migrate
from .core.model_manager import ModelManager
from .core.preprocessors import MedicalImagePreprocessor

def create_app(config_class=Config):
    """
    App Factory: Creates and returns initialized Flask instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize storage directories
    config_class.init_app(app)

    # Setup Logging
    logging.basicConfig(level=logging.INFO)
    app.logger.info("Initializing MedVision-AI Backend Foundation...")

    # 1. Initialize database and core extensions
    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    migrate.init_app(app, db)

    # 2. Register core pipeline engines inside extension dictionary
    app.extensions['model_manager'] = ModelManager(app)
    app.extensions['preprocessor'] = MedicalImagePreprocessor()

    # 3. Create database tables directly on startup (simplifies academic setup)
    with app.app_context():
        db.create_all()
        app.logger.info("Database schemas compiled successfully.")

    # 4. Register API blueprints under standard api prefix
    from .api.models import models_bp
    from .api.diagnostics import diagnostics_bp

    app.register_blueprint(models_bp, url_prefix='/api/v1')
    app.register_blueprint(diagnostics_bp, url_prefix='/api/v1')

    app.logger.info("REST API blueprints registered successfully under /api/v1 prefix.")

    return app
