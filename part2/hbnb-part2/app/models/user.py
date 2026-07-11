"""User entity class."""
import re
from app.models.base_model import BaseModel
from app import bcrypt


class User(BaseModel):
    """Represent a user with secure password hashing via bcrypt."""

    def __init__(self, first_name, last_name, email,
                 password="", is_admin=False):
        """Initialize a User instance.

        Args:
            first_name (str): The user's first name.
            last_name (str): The user's last name.
            email (str): The user's email address.
            password (str): The user's plaintext password (will be hashed).
            is_admin (bool): Whether the user has admin privileges.
        """
        super().__init__()
        self.first_name = self._validate_name(first_name, "first_name")
        self.last_name = self._validate_name(last_name, "last_name")
        self.email = self._validate_email(email)
        self.is_admin = is_admin
        self.password = ""
        if password:
            self.hash_password(password)
        self.places = []
        self.reviews = []

    @staticmethod
    def _validate_name(value, field_name):
        """Validate that a name field is a non-empty string under 50 chars.

        Args:
            value (str): The value to validate.
            field_name (str): The field name for error messages.

        Returns:
            str: The validated value.
        """
        if not value or not isinstance(value, str):
            raise ValueError(f"{field_name} is required")
        if len(value) > 50:
            raise ValueError(f"{field_name} must be 50 characters or fewer")
        return value

    @staticmethod
    def _validate_email(email):
        """Validate that the email is a properly formatted string.

        Args:
            email (str): The email address to validate.

        Returns:
            str: The validated email address.
        """
        if not email or not isinstance(email, str):
            raise ValueError("email is required")
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(pattern, email):
            raise ValueError("email format is invalid")
        return email

    def hash_password(self, password):
        """Hash a plaintext password and store it in the password field.

        Args:
            password (str): The plaintext password to hash.
        """
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify a plaintext password against the stored hashed password.

        Args:
            password (str): The plaintext password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return bcrypt.check_password_hash(self.password, password)

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
