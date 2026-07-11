"""User-specific repository for database operations."""
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """Repository for User-specific database operations."""

    def __init__(self):
        """Initialize the UserRepository with the User model."""
        super().__init__(User)

    def get_user_by_email(self, email):
        """Retrieve a user by their email address.

        Args:
            email (str): The email address to search for.

        Returns:
            User: The matching user, or None if not found.
        """
        return self.model.query.filter_by(email=email).first()
