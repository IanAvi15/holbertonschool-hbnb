"""Amenity entity class."""
from app import db
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Represent an amenity that can be associated with places."""

    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        """Initialize an Amenity instance.

        Args:
            name (str): The name of the amenity.
        """
        super().__init__()
        self.name = self._validate_name(name)

    @staticmethod
    def _validate_name(value):
        """Validate the name is a non-empty string under 50 chars."""
        if not value or not isinstance(value, str):
            raise ValueError("name is required")
        if len(value) > 50:
            raise ValueError("name must be 50 characters or fewer")
        return value
