#!/usr/bin/python3
"""Simple tests for the core business logic classes."""
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


def test_user_creation():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False
    print("User creation test passed!")


def test_user_invalid_email():
    try:
        User(first_name="Bad", last_name="Email", email="not-an-email")
        print("User invalid email test FAILED (no exception raised)")
    except ValueError:
        print("User invalid email test passed!")


def test_place_creation():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Cozy Apartment", description="A nice place to stay",
                  price=100, latitude=37.7749, longitude=-122.4194, owner=owner)

    review = Review(text="Great stay!", rating=5, place=place, user=owner)
    place.add_review(review)

    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.reviews) >= 1
    assert place.reviews[-1].text == "Great stay!"
    assert place in owner.places
    print("Place creation and relationship test passed!")


def test_place_invalid_latitude():
    owner = User(first_name="Bad", last_name="Coords", email="bad.coords@example.com")
    try:
        Place(title="Bad Place", description="", price=50,
              latitude=999, longitude=0, owner=owner)
        print("Place invalid latitude test FAILED (no exception raised)")
    except ValueError:
        print("Place invalid latitude test passed!")


def test_review_invalid_rating():
    owner = User(first_name="Rate", last_name="Tester", email="rate.tester@example.com")
    place = Place(title="Test Place", description="", price=50,
                  latitude=0, longitude=0, owner=owner)
    try:
        Review(text="Bad rating", rating=10, place=place, user=owner)
        print("Review invalid rating test FAILED (no exception raised)")
    except ValueError:
        print("Review invalid rating test passed!")


def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    print("Amenity creation test passed!")


def test_place_amenity_relationship():
    owner = User(first_name="Amen", last_name="Ity", email="amen.ity@example.com")
    place = Place(title="Amenity Place", description="", price=75,
                  latitude=0, longitude=0, owner=owner)
    wifi = Amenity(name="Wi-Fi")
    place.add_amenity(wifi)
    assert wifi in place.amenities
    print("Place-Amenity relationship test passed!")


def test_update_method():
    user = User(first_name="Update", last_name="Me", email="update.me@example.com")
    old_updated_at = user.updated_at
    user.update({"first_name": "Updated"})
    assert user.first_name == "Updated"
    assert user.updated_at >= old_updated_at
    print("BaseModel update() test passed!")


if __name__ == "__main__":
    test_user_creation()
    test_user_invalid_email()
    test_place_creation()
    test_place_invalid_latitude()
    test_review_invalid_rating()
    test_amenity_creation()
    test_place_amenity_relationship()
    test_update_method()
    print("\nAll tests completed.")
