"""Review entity class."""
from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)
        self.place = self._validate_place(place)
        self.user = self._validate_user(user)

        # Keep the related place and user lists in sync
        self.place.add_review(self)
        self.user.add_review(self)

    @staticmethod
    def _validate_text(value):
        if not value or not isinstance(value, str):
            raise ValueError("text is required")
        return value

    @staticmethod
    def _validate_rating(value):
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError("rating must be an integer")
        if not (1 <= value <= 5):
            raise ValueError("rating must be between 1 and 5")
        return value

    @staticmethod
    def _validate_place(place):
        if not isinstance(place, Place):
            raise ValueError("place must be a valid Place instance")
        return place

    @staticmethod
    def _validate_user(user):
        if not isinstance(user, User):
            raise ValueError("user must be a valid User instance")
        return user

    def update(self, data):
        """Update attributes, re-validating text/rating/place/user."""
        if 'text' in data:
            data['text'] = self._validate_text(data['text'])
        if 'rating' in data:
            data['rating'] = self._validate_rating(data['rating'])
        if 'place' in data:
            data['place'] = self._validate_place(data['place'])
        if 'user' in data:
            data['user'] = self._validate_user(data['user'])
        super().update(data)
