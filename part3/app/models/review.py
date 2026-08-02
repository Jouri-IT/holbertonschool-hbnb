#!/usr/bin/python3

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    """Review model.

    Attributes per Part 2 design: rating, text, place, user. The
    actual Place/User objects are kept as the relationship attributes
    (not just their ids) so the review always references a live,
    validated instance. place_id/user_id remain available as
    read-only properties derived from those objects, since the rest
    of the codebase (facade, API layer) addresses reviews by id.

    Registering the review with its place (place.add_review()) is the
    caller's responsibility, not this constructor's -- callers that
    already hold the place object are expected to link it explicitly.
    """

    def __init__(self, text, rating, place, user):
        super().__init__()

        if not isinstance(place, Place):
            raise TypeError("place must be a Place")
        if not isinstance(user, User):
            raise TypeError("user must be a User")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        self.validate()

    @property
    def place_id(self):
        """Id of the referenced place, derived from the place object."""
        return self.place.id

    @property
    def user_id(self):
        """Id of the reviewing user, derived from the user object."""
        return self.user.id

    def validate(self):
        """Validate review attributes."""

        if not isinstance(self.text, str):
            raise TypeError("text must be a string")
        if len(self.text) == 0:
            raise ValueError("text cannot be empty")

        # bool is a subclass of int in Python, so this must be checked
        # explicitly or True/False would silently pass as 1/0.
        if not isinstance(self.rating, int) or isinstance(self.rating, bool):
            raise TypeError("rating must be an integer")
        if self.rating < 1 or self.rating > 5:
            raise ValueError("rating must be between 1 and 5")

        if not isinstance(self.place, Place):
            raise TypeError("place must be a Place")
        if not isinstance(self.user, User):
            raise TypeError("user must be a User")

    def to_dict(self):
        """Return dictionary representation with flattened relationships."""
        data = super().to_dict()
        data.pop("place", None)
        data.pop("user", None)
        data["place_id"] = self.place_id
        data["user_id"] = self.user_id
        return data

    @staticmethod
    def list_by_place(reviews, place_id):
        """Return all reviews from a collection matching a given place_id.

        Matches list_by_place() from the Part 1 diagram.
        """
        return [r for r in reviews if r.place_id == place_id]
