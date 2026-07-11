"""Place-related API endpoints."""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenity IDs")
})


def _serialize_owner(owner):
    """Serialize an owner object to a dictionary."""
    return {
        'id': owner.id,
        'first_name': owner.first_name,
        'last_name': owner.last_name,
        'email': owner.email
    }


def _serialize_amenity(amenity):
    """Serialize an amenity object to a dictionary."""
    return {
        'id': amenity.id,
        'name': amenity.name
    }


def _serialize_review(review):
    """Serialize a review object to a dictionary."""
    return {
        'id': review.id,
        'text': review.text,
        'rating': review.rating,
        'user_id': review.user.id
    }


def _serialize_review_summary(review):
    """Slim review representation matching the place-reviews list example."""
    return {
        'id': review.id,
        'text': review.text,
        'rating': review.rating
    }


def _serialize_summary(place):
    """Slim representation used for the place list endpoint."""
    return {
        'id': place.id,
        'title': place.title,
        'latitude': place.latitude,
        'longitude': place.longitude
    }


def _serialize_detail(place):
    """Full representation used for the place detail endpoint."""
    return {
        'id': place.id,
        'title': place.title,
        'description': place.description,
        'price': place.price,
        'latitude': place.latitude,
        'longitude': place.longitude,
        'owner': _serialize_owner(place.owner),
        'amenities': [_serialize_amenity(a) for a in place.amenities],
        'reviews': [_serialize_review(r) for r in place.reviews]
    }


@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_input_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place (authenticated users only)"""
        current_user_id = get_jwt_identity()
        place_data = api.payload
        place_data['owner_id'] = current_user_id
        try:
            new_place = facade.create_place(place_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        return _serialize_detail(new_place), 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places (public)"""
        places = facade.get_all_places()
        return [_serialize_summary(place) for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID (public)"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return _serialize_detail(place), 200

    @jwt_required()
    @api.expect(place_input_model)
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information (owner only)"""
        current_user_id = get_jwt_identity()
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        if place.owner.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        place_data = api.payload
        try:
            facade.update_place(place_id, place_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        return {'message': 'Place updated successfully'}, 200


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place (public)"""
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {'error': 'Place not found'}, 404
        return [_serialize_review_summary(r) for r in reviews], 200
    