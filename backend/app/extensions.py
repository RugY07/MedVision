from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

# Initialize extension instances
db = SQLAlchemy()
cors = CORS()
migrate = Migrate()
