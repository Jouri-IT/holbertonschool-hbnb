#!/usr/bin/python3

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    """Review model.

    Attributes per Part 1 design: rating, comment, user_id, place_id.
    The actual Place/User objects are required at construction time so
    they can be validated (they must already exist), but only their
    ids are stored as the persisted relationship attributes.
    """

    def __init__(self, comment, rating, place, user):
        super().__init__()

        if not isinstance(place, Place):
            raise TypeError("place must be a Place")
        if not isinstance(user, User):
            raise TypeError("user must be a User")

        self.comment = comment
        self.rating = rating
        self.place_id = place.id
        self.user_id = user.id

        self.validate()

        # Linking a Review to its Place, per the "seamless interactions"
        # requirement -- creating a Review automatically registers it.
        place.add_review(self)

    def validate(self):
        """Validate review attributes."""

        if not isinstance(self.comment, str):
            raise TypeError("comment must be a string")
        if len(self.comment) == 0:
            raise ValueError("comment cannot be empty")

        # bool is a subclass of int in Python, so this must be checked
        # explicitly or True/False would silently pass as 1/0.
        if not isinstance(self.rating, int) or isinstance(self.rating, bool):
            raise TypeError("rating must be an integer")
        if self.rating < 1 or self.rating > 5:
            raise ValueError("rating must be between 1 and 5")

        if not isinstance(self.place_id, str) or not self.place_id:
            raise ValueError("place_id is required")
        if not isinstance(self.user_id, str) or not self.user_id:
            raise ValueError("user_id is required")

    @staticmethod
    def list_by_place(reviews, place_id):
        """Return all reviews from a collection matching a given place_id.

        Matches list_by_place() from the Part 1 diagram.
        """
        return [r for r in reviews if r.place_id == place_id]
