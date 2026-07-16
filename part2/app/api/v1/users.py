#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Single shared model for both POST and PUT, matching the task spec
# exactly (first_name, last_name, email -- no password, no is_admin).
# Responses are built as plain dicts with the same three fields plus
# id, also per spec: no is_admin/timestamps/password are ever returned.
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
})


def user_output(user):
    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }


@api.route('/')
class UserList(Resource):

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve the list of all users"""
        users = facade.get_all_users()
        return [user_output(user) for user in users], 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real
        # validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

        return user_output(new_user), 201


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

    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update an existing user's information"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        user_data = api.payload

        # If the email is changing, make sure it isn't already taken
        # by a different user.
        new_email = user_data.get('email')
        if new_email and new_email != user.email:
            existing_user = facade.get_user_by_email(new_email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already registered'}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

        return user_output(updated_user), 200
