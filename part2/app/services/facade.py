from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # --- User Operations ---
    def register_user(self, user_data):
        """Register a new user account."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Fetch a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Fetch a user by email address."""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieve all registered users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update an existing user's information."""
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(user_data)
        return user

    # --- Amenity Operations ---
    def create_amenity(self, amenity_data):
        """Create and register a new amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Fetch an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all registered amenities."""
        return self.amenity_repo.get_all()

    def list_amenities(self):
        """List all amenities (alias for get_all_amenities)."""
        return self.get_all_amenities()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        return amenity

    def delete_amenity(self, amenity_id):
        """Delete an amenity by ID."""
        self.amenity_repo.delete(amenity_id)

    # --- Place Operations ---
    def create_place(self, place_data):
        """Create and register a new place listing."""
        # place_data should contain owner_id; fetch the User object
        owner_id = place_data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner user does not exist")
        
        # Remove owner_id from data; Place constructor takes owner object
        place_data_copy = place_data.copy()
        place_data_copy.pop('owner_id', None)
        place_data_copy['owner'] = owner
        
        place = Place(**place_data_copy)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Fetch a place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places."""
        return self.place_repo.get_all()

    def list_places(self, filters=None):
        """List all places with optional filtering.
        
        Filters could include: price_min, price_max, latitude, longitude, etc.
        Per Part 1 Fig 6, filtering is done by the facade/model, not the repo.
        """
        places = self.place_repo.get_all()
        
        if not filters:
            return places
        
        # Apply filtering logic here (minimal for now)
        filtered = places
        if 'price_min' in filters:
            filtered = [p for p in filtered if p.price >= filters['price_min']]
        if 'price_max' in filters:
            filtered = [p for p in filtered if p.price <= filters['price_max']]
        
        return filtered

    def update_place(self, place_id, place_data):
        """Update an existing place."""
        place = self.place_repo.get(place_id)
        if not place:
            return None
        place.update(place_data)
        return place

    # --- Review Operations ---
    def submit

