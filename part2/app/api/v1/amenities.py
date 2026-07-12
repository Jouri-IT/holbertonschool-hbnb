#!/usr/bin/python3
from flask import request
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
        data = request.get_json()
        
        # Check if amenity name already exists to prevent duplicates
        existing_amenities = facade.get_all_amenities()
        if any(a.name.lower() == data['name'].lower() for a in existing_amenities):
            return {'error': 'Amenity name already exists'}, 400
            
        try:
            new_amenity = facade.create_amenity(data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities successfully retrieved')
    def get(self):
        """Retrieve all amenities"""
        amenities = facade.get_all_amenities()
        return [{'id': a.id, 'name': a.name} for a in amenities], 200


@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details successfully retrieved')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity successfully updated')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input')
    def edit(self, amenity_id): # Using edit/put based on flask-restx patterns
        pass
        
    def put(self, amenity_id):
        """Update an amenity's information"""
        data = request.get_json()
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
            
        try:
            updated_amenity = facade.update_amenity(amenity_id, data)
            return {'id': updated_amenity.id, 'name': updated_amenity.name}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
