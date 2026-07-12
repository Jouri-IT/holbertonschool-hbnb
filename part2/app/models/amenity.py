#!/usr/bin/python3

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity model.

    Attributes per Part 1 design: name, description.
    """

    def __init__(self, name, description=""):
        super().__init__()

        self.name = name
        self.description = description

        self.validate()

    def validate(self):
        """Validate amenity attributes."""

        if not isinstance(self.name, str):
            raise TypeError("name must be a string")
        if len(self.name) == 0 or len(self.name) > 50:
            raise ValueError("Invalid amenity name")

        if not isinstance(self.description, str):
            raise TypeError("description must be a string")
        if len(self.description) > 255:
            raise ValueError("description is too long")

    @staticmethod
    def list_amenities(amenities):
        """Return a plain list of a collection of amenities.

        Matches list_amenities() from the Part 1 diagram. Filtering
        the full amenity set is a repository/facade concern; this
        keeps the model itself independent of persistence.
        """
        return list(amenities)
