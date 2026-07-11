"""Base model providing shared id and timestamp attributes."""
import uuid
from datetime import datetime
from app import db


class BaseModel(db.Model):
    """Abstract base model with shared id and timestamp columns."""

    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def save(self):
        """Update the updated_at timestamp and commit to the database."""
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def update(self, data):
        """Update the attributes of the object based on a dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
