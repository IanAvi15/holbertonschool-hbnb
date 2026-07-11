"""Place entity class."""
from app import db
from app.models.base_model import BaseModel


class Place(BaseModel):
    """Represent a place listing with location and pricing details."""

    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(self, title, price, latitude, longitude,
                 owner, description=None):
        """Initialize a Place instance.

        Args:
            title (str): Title of the place.
            price (float): Price per night.
            latitude (float): Latitude coordinate.
            longitude (float): Longitude coordinate.
            owner (User): The user who owns the place.
            description (str): Optional description of the place.
        """
        super().__init__()
        self.title = self._validate_title(title)
        self.description = description if description is not None else ""
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.owner = owner
        self.reviews = []
        self.amenities = []

    @staticmethod
    def _validate_title(value):
        """Validate the title is a non-empty string under 100 chars."""
        if not value or not isinstance(value, str):
            raise ValueError("title is required")
        if len(value) > 100:
            raise ValueError("title must be 100 characters or fewer")
        return value

    @staticmethod
    def _validate_price(value):
        """Validate the price is a positive number."""
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError("price must be a number")
        if value <= 0:
            raise ValueError("price must be a positive value")
        return float(value)

    @staticmethod
    def _validate_latitude(value):
        """Validate the latitude is between -90 and 90."""
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError("latitude must be a number")
        if not (-90.0 <= value <= 90.0):
            raise ValueError("latitude must be between -90.0 and 90.0")
        return float(value)

    @staticmethod
    def _validate_longitude(value):
        """Validate the longitude is between -180 and 180."""
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError("longitude must be a number")
        if not (-180.0 <= value <= 180.0):
            raise ValueError("longitude must be between -180.0 and 180.0")
        return float(value)

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