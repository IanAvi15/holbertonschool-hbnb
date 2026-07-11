"""User entity class."""
import re
from app import db, bcrypt
from app.models.base_model import BaseModel


class User(BaseModel):
    """Represent a user with secure password hashing via bcrypt."""

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

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

    @staticmethod
    def _validate_name(value, field_name):
        """Validate that a name field is a non-empty string under 50 chars."""
        if not value or not isinstance(value, str):
            raise ValueError(f"{field_name} is required")
        if len(value) > 50:
            raise ValueError(f"{field_name} must be 50 characters or fewer")
        return value

    @staticmethod
    def _validate_email(email):
        """Validate that the email is a properly formatted string."""
        if not email or not isinstance(email, str):
            raise ValueError("email is required")
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(pattern, email):
            raise ValueError("email format is invalid")
        return email

    def hash_password(self, password):
        """Hash a plaintext password and store it in the password field."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify a plaintext password against the stored hashed password."""
        return bcrypt.check_password_hash(self.password, password)
