#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and API documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity (e.g., Wi-Fi, Pool)')
})


@api.route('/')
class AmenityList(Resource):

    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input or amenity name already exists')
    def post(self):
        """Register a new amenity"""
        data = api.payload

        # Check if amenity name already exists to prevent duplicates
        existing_amenities = facade.get_all_amenities()
        if any(a.name.lower() == data['name'].lower() for a in existing_amenities):
            return {'error': 'Amenity name already exists'}, 400

        try:
            new_amenity = facade.create_amenity(data)
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

        return {'id': new_amenity.id, 'name': new_amenity.name}, 201

    @api.response(200, 'List of amenities successfully retrieved')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': a.id, 'name': a.name} for a in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):

    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        data = api.payload

        # If the name is changing, make sure it isn't already taken
        # by a different amenity.
        new_name = data.get('name')
        if new_name and new_name.lower() != amenity.name.lower():
            existing_amenities = facade.get_all_amenities()
            if any(a.name.lower() == new_name.lower() and a.id != amenity_id
                   for a in existing_amenities):
                return {'error': 'Amenity name already exists'}, 400

        try:
            facade.update_amenity(amenity_id, data)
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

        return {'message': 'Amenity updated successfully'}, 200
