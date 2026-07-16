#!/usr/bin/python3

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity


class Place(BaseModel):
    """Place model."""

    def __init__(self, title, price, latitude, longitude, owner,
                 description=None):
        super().__init__()

        if not isinstance(owner, User):
            raise TypeError("owner must be a User")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

        # The owner object is kept for convenience within a single
        # process (e.g. serializing owner name later); owner_id is
        # the actual relationship attribute per the Part 1 design.
        self.owner = owner
        self.owner_id = owner.id

        self.reviews = []
        self.amenities = []

        self.validate()

    def validate(self):
        """Validate place attributes."""

        if not isinstance(self.title, str):
            raise TypeError("title must be a string")
        if len(self.title) == 0 or len(self.title) > 100:
            raise ValueError("Invalid title")

        if self.description is not None and \
                not isinstance(self.description, str):
            raise TypeError("description must be a string")

        if not isinstance(self.price, (int, float)) or \
                isinstance(self.price, bool):
            raise TypeError("price must be a number")
        if self.price <= 0:
            raise ValueError("price must be positive")

        if not isinstance(self.latitude, (int, float)) or \
                isinstance(self.latitude, bool):
            raise TypeError("latitude must be a number")
        if not (-90.0 <= self.latitude <= 90.0):
            raise ValueError("Invalid latitude")

        if not isinstance(self.longitude, (int, float)) or \
                isinstance(self.longitude, bool):
            raise TypeError("longitude must be a number")
        if not (-180.0 <= self.longitude <= 180.0):
            raise ValueError("Invalid longitude")

        if not isinstance(self.owner, User):
            raise TypeError("owner must be a User")

    def add_review(self, review):
        """Add review to place."""
        # Imported locally to avoid a circular import: review.py
        # already imports Place at module load time.
        from app.models.review import Review
        if not isinstance(review, Review):
            raise TypeError("review must be a Review")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add amenity to place."""
        if not isinstance(amenity, Amenity):
            raise TypeError("amenity must be an Amenity")
        self.amenities.append(amenity)

    def to_dict(self):
        """Return dictionary representation with flattened relationships."""
        data = super().to_dict()
        data.pop("owner", None)
        data["owner_id"] = self.owner_id
        data["reviews"] = [review.id for review in self.reviews]
        data["amenities"] = [amenity.id for amenity in self.amenities]
        return data
