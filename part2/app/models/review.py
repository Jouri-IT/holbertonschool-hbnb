#!/usr/bin/python3

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    """Review model."""

    def __init__(self, comment, rating, place, user):
        super().__init__()

        self.comment = comment
        self.rating = rating
        self.place = place
        self.user = user

        self.validate()

    def validate(self):
        """Validate review attributes."""

        if not isinstance(self.comment, str):
            raise TypeError("comment must be a string")

        if len(self.comment) == 0:
            raise ValueError("comment cannot be empty")

        if not isinstance(self.rating, int):
            raise TypeError("rating must be an integer")

        if self.rating < 1 or self.rating > 5:
            raise ValueError("rating must be between 1 and 5")

        if not isinstance(self.place, Place):
            raise TypeError("place must be a Place")

        if not isinstance(self.user, User):
            raise TypeError("user must be a User")
