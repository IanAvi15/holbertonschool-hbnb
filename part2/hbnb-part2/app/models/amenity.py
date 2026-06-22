"""Amenity entity class."""
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = self._validate_name(name)

    @staticmethod
    def _validate_name(value):
        if not value or not isinstance(value, str):
            raise ValueError("name is required")
        if len(value) > 50:
            raise ValueError("name must be 50 characters or fewer")
        return value
