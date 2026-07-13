#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Input model for creating a user (POST). Password is optional here
# since Part 2 registration doesn't require it (auth arrives in Part
# 3); it's never part of any response body either way.
user_creation_model = api.model('UserCreation', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=False, description='Password of the user'),
})

# Input model for updating a user (PUT). Password intentionally left
# out here too -- password changes belong on their own dedicated
# endpoint/flow, not a general profile update, and this keeps it out
# of the docs/expect payload for PUT.
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
    'email': fields.String(required=False, description='Email of the user'),
})

# Output model. No password field exists here at all, so even if a
# stray value made it this far, flask-restx would strip it on the way
# out. This is on top of (not instead of) User.to_dict() already
# excluding password.
user_response_model = api.model('User', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'is_admin': fields.Boolean(description='Whether the user is an admin'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp'),
})


@api.route('/')
class UserList(Resource):

    @api.response(200, 'List of users retrieved successfully')
    @api.marshal_list_with(user_response_model)
    def get(self):
        """Retrieve the list of all users"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

    @api.expect(user_creation_model, validate=True)
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
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

        return new_user.to_dict(), 201


@api.route('/<user_id>')
class UserResource(Resource):

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_update_model, validate=True)
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

        return updated_user.to_dict(), 200
