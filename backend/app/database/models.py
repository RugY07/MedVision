from datetime import datetime
import json
from ..extensions import db

class Scan(db.Model):
    """
    Scan model: Stores original scan properties, types, and upload timestamps.
    """
    __tablename__ = 'scans'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(255), nullable=False)
    scan_type = db.Column(db.String(50), nullable=False)  # brain | bone | chest | cardiac
    upload_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # One-to-one relationship to the analysis results with cascade delete
    analysis = db.relationship(
        'AnalysisResult', 
        back_populates='scan', 
        uselist=False, 
        cascade='all, delete-orphan'
    )

    def to_dict(self):
        """Converts database values into dictionary schema."""
        return {
            'id': self.id,
            'filename': self.filename,
            'scan_type': self.scan_type,
            'upload_time': self.upload_time.isoformat()
        }


class AnalysisResult(db.Model):
    """
    AnalysisResult model: Stores serialized prediction data and paths to local overlays.
    """
    __tablename__ = 'analysis_results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scan_id = db.Column(db.Integer, db.ForeignKey('scans.id'), nullable=False, unique=True)
    prediction = db.Column(db.Text, nullable=False)  # Serialized JSON string
    confidence = db.Column(db.Float, nullable=False)
    processing_time = db.Column(db.Float, nullable=False)
    model_used = db.Column(db.String(100), nullable=False)
    result_image = db.Column(db.String(255), nullable=True)  # Local results overlay file name
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    scan = db.relationship('Scan', back_populates='analysis')

    @property
    def parsed_prediction(self):
        """Retrieves and parses prediction JSON string into Python object."""
        try:
            return json.loads(self.prediction)
        except (ValueError, TypeError):
            return self.prediction

    @parsed_prediction.setter
    def parsed_prediction(self, val):
        """Encodes Python object into JSON string format for database persistence."""
        self.prediction = json.dumps(val)

    def to_dict(self):
        """Converts model parameters to JSON-serializable dictionary."""
        return {
            'id': self.id,
            'scan_id': self.scan_id,
            'prediction': self.parsed_prediction,
            'confidence': self.confidence,
            'processing_time': self.processing_time,
            'model_used': self.model_used,
            'result_image': self.result_image,
            'created_at': self.created_at.isoformat()
        }
