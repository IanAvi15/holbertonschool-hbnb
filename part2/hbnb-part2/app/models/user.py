"""User entity class."""
import re
from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = self._validate_name(first_name, "first_name")
        self.last_name = self._validate_name(last_name, "last_name")
        self.email = self._validate_email(email)
        self.is_admin = is_admin
        self.places = []  # List of places owned by this user
        self.reviews = []  # List of reviews written by this user

    @staticmethod
    def _validate_name(value, field_name):
        if not value or not isinstance(value, str):
            raise ValueError(f"{field_name} is required")
        if len(value) > 50:
            raise ValueError(f"{field_name} must be 50 characters or fewer")
        return value

    @staticmethod
    def _validate_email(email):
        if not email or not isinstance(email, str):
            raise ValueError("email is required")
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(pattern, email):
            raise ValueError("email format is invalid")
        return email

    def add_place(self, place):
        """Add a place owned by this user."""
        self.places.append(place)

    def add_review(self, review):
        """Add a review written by this user."""
        self.reviews.append(review)

    def remove_review(self, review):
        """Remove a review from this user's list, if present."""
        if review in self.reviews:
            self.reviews.remove(review)
