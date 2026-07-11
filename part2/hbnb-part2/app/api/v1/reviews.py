"""Review-related API endpoints."""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)')
})


def _serialize(review):
    """Serialize a review object to a dictionary."""
    return {
        'id': review.id,
        'text': review.text,
        'rating': review.rating,
        'user_id': review.user.id,
        'place_id': review.place.id
    }


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def post(self):
        """Register a new review (authenticated users only)"""
        current_user_id = get_jwt_identity()
        review_data = api.payload

        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 400
        if place.owner.id == current_user_id:
            return {'error': 'You cannot review your own place'}, 400

        existing_reviews = facade.get_reviews_by_place(review_data['place_id'])
        if any(r.user.id == current_user_id for r in existing_reviews):
            return {'error': 'You have already reviewed this place'}, 400

        review_data['user_id'] = current_user_id
        try:
            new_review = facade.create_review(review_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        return _serialize(new_review), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [_serialize(review) for review in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return _serialize(review), 200

    @jwt_required()
    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review (author only)"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if review.user.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.update_review(review_id, api.payload)
        except ValueError as e:
            return {'error': str(e)}, 400
        return {'message': 'Review updated successfully'}, 200

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review (author only)"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if review.user.id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200
    