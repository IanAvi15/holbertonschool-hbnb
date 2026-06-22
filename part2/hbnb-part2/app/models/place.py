"""Place entity class."""
from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner, description=None):
        super().__init__()
        self.title = self._validate_title(title)
        self.description = description if description is not None else ""
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.owner = self._validate_owner(owner)
        self.reviews = []  # List of reviews for this place
        self.amenities = []  # List of amenities for this place

        # Keep the owner's own place list in sync
        self.owner.add_place(self)

    @staticmethod
    def _validate_title(value):
        if not value or not isinstance(value, str):
            raise ValueError("title is required")
        if len(value) > 100:
            raise ValueError("title must be 100 characters or fewer")
        return value

    @staticmethod
    def _validate_price(value):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError("price must be a number")
        if value <= 0:
            raise ValueError("price must be a positive value")
        return float(value)

    @staticmethod
    def _validate_latitude(value):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError("latitude must be a number")
        if not (-90.0 <= value <= 90.0):
            raise ValueError("latitude must be between -90.0 and 90.0")
        return float(value)

    @staticmethod
    def _validate_longitude(value):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError("longitude must be a number")
        if not (-180.0 <= value <= 180.0):
            raise ValueError("longitude must be between -180.0 and 180.0")
        return float(value)

    @staticmethod
    def _validate_owner(owner):
        if not isinstance(owner, User):
            raise ValueError("owner must be a valid User instance")
        return owner

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def remove_review(self, review):
        """Remove a review from the place, if present."""
        if review in self.reviews:
            self.reviews.remove(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
