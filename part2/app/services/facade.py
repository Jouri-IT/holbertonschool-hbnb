from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity  # Import the Amenity model


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # --- User Operations ---
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieve every user. Needed for GET /api/v1/users/."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(user_data)
        return user

    # --- Amenity Operations ---
    def create_amenity(self, amenity_data):
        """Instantiates and registers a new amenity into memory."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Fetches a specific amenity by its UUID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Returns all registered amenities. Needed for GET /api/v1/amenities/."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Updates attributes of an existing amenity."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        return amenity

    # --- Place Operations (Placeholders) ---
    def get_place(self, place_id):
        # Implementation will be added in future tasks
        pass
