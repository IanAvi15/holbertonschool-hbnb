"""Review entity class."""
from app import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    """Represent a user review for a place."""

    __tablename__ = 'reviews'

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, text, rating, place, user):
        """Initialize a Review instance.

        Args:
            text (str): The review text.
            rating (int): Rating from 1 to 5.
            place (Place): The place being reviewed.
            user (User): The user writing the review.
        """
        super().__init__()
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)
        self.place = place
        self.user = user

    @staticmethod
    def _validate_text(value):
        """Validate the review text is a non-empty string."""
        if not value or not isinstance(value, str):
            raise ValueError("text is required")
        return value

    @staticmethod
    def _validate_rating(value):
        """Validate the rating is an integer between 1 and 5."""
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError("rating must be an integer")
        if not (1 <= value <= 5):
            raise ValueError("rating must be between 1 and 5")
        return value

    def update(self, data):
        """Update attributes, re-validating text and rating.

        Args:
            data (dict): Dictionary of attributes to update.
        """
        if 'text' in data:
            data['text'] = self._validate_text(data['text'])
        if 'rating' in data:
            data['rating'] = self._validate_rating(data['rating'])
        super().update(data)
