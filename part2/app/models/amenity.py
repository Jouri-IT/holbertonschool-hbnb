#!/usr/bin/python3

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity model."""

    def __init__(self, name):
        super().__init__()

        self.name = name

        self.validate()

    def validate(self):
        """Validate amenity attributes."""

        if not isinstance(self.name, str):
            raise TypeError("name must be a string")

        if len(self.name) == 0 or len(self.name) > 50:
            raise ValueError("Invalid amenity name")
