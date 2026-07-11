"""User-related API endpoints."""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
})


def _serialize(user):
    """Serialize a user object to a dictionary, excluding the password."""
    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }


@api.route('/')
class UserList(Resource):
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve the list of all users"""
        users = facade.get_all_users()
        return [_serialize(user) for user in users], 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return _serialize(new_user), 201


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return _serialize(user), 200

    @jwt_required()
    @api.expect(update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user details (own account only, no email or password)"""
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        user_data = api.payload
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify email or password'}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return _serialize(updated_user), 200
