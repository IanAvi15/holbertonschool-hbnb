#!/usr/bin/python3
"""Automated tests for the HBnB API endpoints.

Covers positive and negative scenarios for Users, Amenities, Places,
and Reviews, including boundary checks, required-field checks, and
error handling for non-existent resources.
"""
import unittest
from app import create_app
from app.services import facade
from app.persistence.repository import InMemoryRepository


class HBnBTestCase(unittest.TestCase):
    """Base test case providing a fresh app/client and common helpers.

    The HBnBFacade is a module-level singleton (by design, for the running
    application), so app = create_app() does NOT give each test a fresh
    in-memory data store on its own. To keep tests isolated from one
    another, the shared facade's repositories are reset before each test.
    """

    def setUp(self):
        facade.user_repo = InMemoryRepository()
        facade.place_repo = InMemoryRepository()
        facade.review_repo = InMemoryRepository()
        facade.amenity_repo = InMemoryRepository()

        self.app = create_app()
        self.client = self.app.test_client()

    def create_user(self, first_name="John", last_name="Doe",
                     email="john.doe@example.com"):
        resp = self.client.post('/api/v1/users/', json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        })
        return resp

    def create_amenity(self, name="Wi-Fi"):
        return self.client.post('/api/v1/amenities/', json={"name": name})

    def create_place(self, owner_id, amenities=None, **overrides):
        payload = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": owner_id,
            "amenities": amenities or []
        }
        payload.update(overrides)
        return self.client.post('/api/v1/places/', json=payload)

    def create_review(self, user_id, place_id, **overrides):
        payload = {
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        }
        payload.update(overrides)
        return self.client.post('/api/v1/reviews/', json=payload)


class TestUserEndpoints(HBnBTestCase):

    def test_create_user_valid(self):
        resp = self.create_user()
        self.assertEqual(resp.status_code, 201)
        self.assertIn('id', resp.json)
        self.assertEqual(resp.json['email'], "john.doe@example.com")

    def test_create_user_missing_fields(self):
        resp = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": ""
        })
        self.assertEqual(resp.status_code, 400)

    def test_create_user_invalid_email_format(self):
        resp = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email"
        })
        self.assertEqual(resp.status_code, 400)

    def test_create_user_empty_first_name(self):
        resp = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Doe",
            "email": "empty.first@example.com"
        })
        self.assertEqual(resp.status_code, 400)

    def test_create_user_duplicate_email(self):
        self.create_user(email="dup@example.com")
        resp = self.create_user(email="dup@example.com")
        self.assertEqual(resp.status_code, 400)

    def test_get_user_by_id(self):
        created = self.create_user().json
        resp = self.client.get(f"/api/v1/users/{created['id']}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['id'], created['id'])

    def test_get_user_not_found(self):
        resp = self.client.get('/api/v1/users/does-not-exist')
        self.assertEqual(resp.status_code, 404)

    def test_get_all_users(self):
        self.create_user(email="list1@example.com")
        self.create_user(email="list2@example.com")
        resp = self.client.get('/api/v1/users/')
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json, list)
        self.assertGreaterEqual(len(resp.json), 2)

    def test_update_user(self):
        created = self.create_user(email="update.me@example.com").json
        resp = self.client.put(f"/api/v1/users/{created['id']}", json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json['first_name'], "Jane")

    def test_update_user_not_found(self):
        resp = self.client.put('/api/v1/users/does-not-exist', json={
            "first_name": "X", "last_name": "Y", "email": "x@y.com"
        })
        self.assertEqual(resp.status_code, 404)


class TestAmenityEndpoints(HBnBTestCase):

    def test_create_amenity_valid(self):
        resp = self.create_amenity()
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json['name'], "Wi-Fi")

    def test_create_amenity_missing_name(self):
        resp = self.client.post('/api/v1/amenities/', json={})
        self.assertEqual(resp.status_code, 400)

    def test_create_amenity_name_too_long(self):
        resp = self.client.post('/api/v1/amenities/', json={
            "name": "X" * 51
        })
        self.assertEqual(resp.status_code, 400)

    def test_get_all_amenities(self):
        self.create_amenity(name="Pool")
        resp = self.client.get('/api/v1/amenities/')
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json, list)

    def test_get_amenity_by_id(self):
        created = self.create_amenity(name="Parking").json
        resp = self.client.get(f"/api/v1/amenities/{created['id']}")
        self.assertEqual(resp.status_code, 200)

    def test_get_amenity_not_found(self):
        resp = self.client.get('/api/v1/amenities/does-not-exist')
        self.assertEqual(resp.status_code, 404)

    def test_update_amenity(self):
        created = self.create_amenity(name="Old Name").json
        resp = self.client.put(f"/api/v1/amenities/{created['id']}", json={
            "name": "New Name"
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"message": "Amenity updated successfully"})

    def test_update_amenity_not_found(self):
        resp = self.client.put('/api/v1/amenities/does-not-exist', json={
            "name": "X"
        })
        self.assertEqual(resp.status_code, 404)


class TestPlaceEndpoints(HBnBTestCase):

    def setUp(self):
        super().setUp()
        self.owner = self.create_user(email="owner@example.com").json
        self.amenity = self.create_amenity(name="Wi-Fi").json

    def test_create_place_valid(self):
        resp = self.create_place(self.owner['id'], amenities=[self.amenity['id']])
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json['owner']['id'], self.owner['id'])
        self.assertEqual(len(resp.json['amenities']), 1)

    def test_create_place_missing_title(self):
        resp = self.client.post('/api/v1/places/', json={
            "price": 50.0, "latitude": 0, "longitude": 0,
            "owner_id": self.owner['id'], "amenities": []
        })
        self.assertEqual(resp.status_code, 400)

    def test_create_place_negative_price(self):
        resp = self.create_place(self.owner['id'], price=-10)
        self.assertEqual(resp.status_code, 400)

    def test_create_place_latitude_out_of_range_high(self):
        resp = self.create_place(self.owner['id'], latitude=91)
        self.assertEqual(resp.status_code, 400)

    def test_create_place_latitude_out_of_range_low(self):
        resp = self.create_place(self.owner['id'], latitude=-91)
        self.assertEqual(resp.status_code, 400)

    def test_create_place_latitude_boundary_valid(self):
        resp = self.create_place(self.owner['id'], latitude=90)
        self.assertEqual(resp.status_code, 201)

    def test_create_place_longitude_out_of_range(self):
        resp = self.create_place(self.owner['id'], longitude=181)
        self.assertEqual(resp.status_code, 400)

    def test_create_place_longitude_boundary_valid(self):
        resp = self.create_place(self.owner['id'], longitude=180)
        self.assertEqual(resp.status_code, 201)

    def test_create_place_nonexistent_owner(self):
        resp = self.create_place("does-not-exist")
        self.assertEqual(resp.status_code, 400)

    def test_create_place_nonexistent_amenity(self):
        resp = self.create_place(self.owner['id'], amenities=["does-not-exist"])
        self.assertEqual(resp.status_code, 400)

    def test_get_place_by_id_includes_owner_and_amenities(self):
        created = self.create_place(self.owner['id'], amenities=[self.amenity['id']]).json
        resp = self.client.get(f"/api/v1/places/{created['id']}")
        self.assertEqual(resp.status_code, 200)
        self.assertIn('owner', resp.json)
        self.assertIn('amenities', resp.json)
        self.assertIn('reviews', resp.json)

    def test_get_place_not_found(self):
        resp = self.client.get('/api/v1/places/does-not-exist')
        self.assertEqual(resp.status_code, 404)

    def test_get_all_places_summary_shape(self):
        self.create_place(self.owner['id'])
        resp = self.client.get('/api/v1/places/')
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json, list)
        if resp.json:
            self.assertIn('id', resp.json[0])
            self.assertIn('title', resp.json[0])
            self.assertNotIn('owner', resp.json[0])

    def test_update_place_partial(self):
        created = self.create_place(self.owner['id']).json
        resp = self.client.put(f"/api/v1/places/{created['id']}", json={
            "title": "Luxury Condo",
            "description": "An upscale place to stay",
            "price": 200.0
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"message": "Place updated successfully"})

    def test_update_place_not_found(self):
        resp = self.client.put('/api/v1/places/does-not-exist', json={
            "title": "X"
        })
        self.assertEqual(resp.status_code, 404)


class TestReviewEndpoints(HBnBTestCase):

    def setUp(self):
        super().setUp()
        self.owner = self.create_user(email="review.owner@example.com").json
        self.reviewer = self.create_user(email="reviewer@example.com").json
        self.place = self.create_place(self.owner['id']).json

    def test_create_review_valid(self):
        resp = self.create_review(self.reviewer['id'], self.place['id'])
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json['user_id'], self.reviewer['id'])
        self.assertEqual(resp.json['place_id'], self.place['id'])

    def test_create_review_missing_text(self):
        resp = self.client.post('/api/v1/reviews/', json={
            "rating": 5,
            "user_id": self.reviewer['id'],
            "place_id": self.place['id']
        })
        self.assertEqual(resp.status_code, 400)

    def test_create_review_rating_too_high(self):
        resp = self.create_review(self.reviewer['id'], self.place['id'], rating=6)
        self.assertEqual(resp.status_code, 400)

    def test_create_review_rating_too_low(self):
        resp = self.create_review(self.reviewer['id'], self.place['id'], rating=0)
        self.assertEqual(resp.status_code, 400)

    def test_create_review_rating_boundary_valid(self):
        resp = self.create_review(self.reviewer['id'], self.place['id'], rating=1)
        self.assertEqual(resp.status_code, 201)

    def test_create_review_nonexistent_user(self):
        resp = self.create_review("does-not-exist", self.place['id'])
        self.assertEqual(resp.status_code, 400)

    def test_create_review_nonexistent_place(self):
        resp = self.create_review(self.reviewer['id'], "does-not-exist")
        self.assertEqual(resp.status_code, 400)

    def test_get_review_by_id(self):
        created = self.create_review(self.reviewer['id'], self.place['id']).json
        resp = self.client.get(f"/api/v1/reviews/{created['id']}")
        self.assertEqual(resp.status_code, 200)

    def test_get_review_not_found(self):
        resp = self.client.get('/api/v1/reviews/does-not-exist')
        self.assertEqual(resp.status_code, 404)

    def test_get_all_reviews_summary_shape(self):
        self.create_review(self.reviewer['id'], self.place['id'])
        resp = self.client.get('/api/v1/reviews/')
        self.assertEqual(resp.status_code, 200)
        if resp.json:
            self.assertIn('text', resp.json[0])
            self.assertIn('rating', resp.json[0])
            self.assertNotIn('user_id', resp.json[0])

    def test_get_reviews_for_place(self):
        self.create_review(self.reviewer['id'], self.place['id'])
        resp = self.client.get(f"/api/v1/places/{self.place['id']}/reviews")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json), 1)

    def test_get_reviews_for_nonexistent_place(self):
        resp = self.client.get('/api/v1/places/does-not-exist/reviews')
        self.assertEqual(resp.status_code, 404)

    def test_update_review_partial(self):
        created = self.create_review(self.reviewer['id'], self.place['id']).json
        resp = self.client.put(f"/api/v1/reviews/{created['id']}", json={
            "text": "Amazing stay!",
            "rating": 4
        })
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"message": "Review updated successfully"})

    def test_update_review_invalid_rating(self):
        created = self.create_review(self.reviewer['id'], self.place['id']).json
        resp = self.client.put(f"/api/v1/reviews/{created['id']}", json={
            "rating": 99
        })
        self.assertEqual(resp.status_code, 400)

    def test_update_review_not_found(self):
        resp = self.client.put('/api/v1/reviews/does-not-exist', json={
            "text": "X"
        })
        self.assertEqual(resp.status_code, 404)

    def test_delete_review(self):
        created = self.create_review(self.reviewer['id'], self.place['id']).json
        resp = self.client.delete(f"/api/v1/reviews/{created['id']}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"message": "Review deleted successfully"})

        # Confirm it is actually gone
        follow_up = self.client.get(f"/api/v1/reviews/{created['id']}")
        self.assertEqual(follow_up.status_code, 404)

    def test_delete_review_not_found(self):
        resp = self.client.delete('/api/v1/reviews/does-not-exist')
        self.assertEqual(resp.status_code, 404)

    def test_delete_review_removes_from_place(self):
        created = self.create_review(self.reviewer['id'], self.place['id']).json
        self.client.delete(f"/api/v1/reviews/{created['id']}")
        place_resp = self.client.get(f"/api/v1/places/{self.place['id']}")
        self.assertEqual(len(place_resp.json['reviews']), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
