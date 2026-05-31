import os
from app import create_app

# Instantiate the Flask Application Factory
app = create_app()

if __name__ == '__main__':
    # Parse running configurations
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    app.logger.info(f"Starting MedVision-AI API server on {host}:{port}...")
    app.run(host=host, port=port, debug=debug)
