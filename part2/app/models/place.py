#!/usr/bin/python3

from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    """Place model."""

    def __init__(self, title, description, price,
                 latitude, longitude, owner):
        super().__init__()

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

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

        if self.price <= 0:
            raise ValueError("price must be positive")

        if not (-90.0 <= self.latitude <= 90.0):
            raise ValueError("Invalid latitude")

        if not (-180.0 <= self.longitude <= 180.0):
            raise ValueError("Invalid longitude")

        if not isinstance(self.owner, User):
            raise TypeError("owner must be a User")

    def add_review(self, review):
        """Add review to place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add amenity to place."""
        self.amenities.append(amenity)
