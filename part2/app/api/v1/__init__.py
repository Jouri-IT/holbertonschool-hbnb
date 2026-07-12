from flask_restx import Api
from flask import Blueprint

blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(blueprint, version='1.0', title='HBnB API', description='HBnB Application RESTful API')

# Import your namespaces
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns

# Register the namespaces
api.add_namespace(users_ns, path='/users')
api.add_namespace(amenities_ns, path='/amenities')
