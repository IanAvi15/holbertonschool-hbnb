"""Facade pattern implementation for coordinating app layers."""
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository
from app.services.repositories.user_repository import UserRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        """Create a new user and store it in the repository."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email address."""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update an existing user's attributes."""
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(user_data)
        return user

    def create_amenity(self, amenity_data):
        """Create a new amenity and store it in the repository."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity's attributes."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        return amenity

    def create_place(self, place_data):
        """Create a new place, resolving owner and amenities by ID."""
        data = dict(place_data)
        owner_id = data.pop('owner_id', None)
        amenity_ids = data.pop('amenities', [])

        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("owner_id does not correspond to an existing user")

        try:
            place = Place(owner=owner, **data)
        except TypeError as e:
            raise ValueError(f"invalid place data: {e}")

        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(
                    f"amenities contains an unknown amenity id: {amenity_id}"
                )
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID, including its owner and amenities."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update an existing place's attributes."""
        place = self.place_repo.get(place_id)
        if not place:
            return None

        data = dict(place_data)

        # Allow re-assigning the owner via owner_id, if provided
        owner_id = data.pop('owner_id', None)
        if owner_id is not None:
            owner = self.user_repo.get(owner_id)
            if not owner:
                raise ValueError("owner_id does not correspond to an existing user")
            data['owner'] = owner

        # Allow re-assigning amenities via a list of IDs, if provided
        amenity_ids = data.pop('amenities', None)
        if amenity_ids is not None:
            amenities = []
            for amenity_id in amenity_ids:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(
                        f"amenities contains an unknown amenity id: {amenity_id}"
                    )
                amenities.append(amenity)
            data['amenities'] = amenities

        place.update(data)
        return place

    def create_review(self, review_data):
        """Create a new review, resolving user_id and place_id by ID."""
        data = dict(review_data)
        user_id = data.pop('user_id', None)
        place_id = data.pop('place_id', None)

        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("user_id does not correspond to an existing user")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("place_id does not correspond to an existing place")

        try:
            review = Review(place=place, user=user, **data)
        except TypeError as e:
            raise ValueError(f"invalid review data: {e}")

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieve all reviews for a specific place."""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place.reviews

    def update_review(self, review_id, review_data):
        """Update an existing review's attributes."""
        review = self.review_repo.get(review_id)
        if not review:
            return None

        data = dict(review_data)

        # Allow re-assigning the user via user_id, if provided
        user_id = data.pop('user_id', None)
        if user_id is not None:
            new_user = self.user_repo.get(user_id)
            if not new_user:
                raise ValueError("user_id does not correspond to an existing user")
            if new_user is not review.user:
                review.user.remove_review(review)
                new_user.add_review(review)
                data['user'] = new_user

        # Allow re-assigning the place via place_id, if provided
        place_id = data.pop('place_id', None)
        if place_id is not None:
            new_place = self.place_repo.get(place_id)
            if not new_place:
                raise ValueError("place_id does not correspond to an existing place")
            if new_place is not review.place:
                review.place.remove_review(review)
                new_place.add_review(review)
                data['place'] = new_place

        review.update(data)
        return review

    def delete_review(self, review_id):
        """Delete a review and remove it from related place/user lists."""
        review = self.review_repo.get(review_id)
        if not review:
            return False

        review.place.remove_review(review)
        review.user.remove_review(review)
        self.review_repo.delete(review_id)
        return True
