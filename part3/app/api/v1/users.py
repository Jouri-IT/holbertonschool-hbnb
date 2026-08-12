#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('users', description='User operations')

# Model used when creating a new user
create_user_model = api.model('CreateUser', {
    'first_name': fields.String(
        required=True,
        description='First name of the user'
    ),
    'last_name': fields.String(
        required=True,
        description='Last name of the user'
    ),
    'email': fields.String(
        required=True,
        description='Email of the user'
    ),
    'password': fields.String(
        required=True,
        description='User password'
    )
})

# Model used when updating a user. email/password are only actually
# accepted when the caller is an admin (see UserResource.put), but
# they're listed here (not required) so admin requests validate too.
update_user_model = api.model('UpdateUser', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='Password of the user')
})


def user_output(user):
    """Return user data without password."""
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
        """Retrieve all users"""
        users = facade.get_all_users()
        return [user_output(user) for user in users], 200

    @jwt_required()
    @api.expect(create_user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Register a new user (admin only)"""

        if not get_jwt().get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

        return {
            'id': new_user.id,
            'message': 'User successfully created'
        }, 201


@api.route('/<user_id>')
class UserResource(Resource):

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""

        user = facade.get_user(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        return user_output(user), 200

    @jwt_required()
    @api.expect(update_user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Email already in use')
    @api.response(403, 'Unauthorized action')
    def put(self, user_id):
        """Update an existing user's information.

        Regular users may only update their own first_name/last_name,
        and may not touch email or password. Admins may update any
        user, including email and password, subject to email
        uniqueness.
        """

        user = facade.get_user(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        is_admin = get_jwt().get('is_admin', False)
        current_user = get_jwt_identity()

        if not is_admin and current_user != user_id:
            return {'error': 'Unauthorized action'}, 403

        user_data = api.payload

        if not is_admin and ('email' in user_data or 'password' in user_data):
            return {'error': 'You cannot modify email or password'}, 400

        email = user_data.get('email')
        if is_admin and email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        try:
            updated_user = facade.update_user(
                user_id, user_data, is_admin=is_admin
            )
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

        return user_output(updated_user), 200
