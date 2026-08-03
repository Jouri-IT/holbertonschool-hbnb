#!/usr/bin/python3

from app import db
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    """Review model.

    Attributes per Part 2 design: rating, text, place, user.

    place_id/user_id are real mapped columns with ForeignKey
    constraints to places.id and users.id. `place`/`user` are
    available automatically via backref from Place.reviews and
    User.reviews, not set manually here.

    Registering the review with its place (place.add_review()) is the
    caller's responsibility, not this constructor's -- callers that
    already hold the place object are expected to link it explicitly.
    """

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, text, rating, place, user):
        super().__init__()

        if not isinstance(place, Place):
            raise TypeError("place must be a Place")
        if not isinstance(user, User):
            raise TypeError("user must be a User")

        self.text = text
        self.rating = rating
        self.place_id = place.id
        self.user_id = user.id

        self.validate()

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

        # place_id/user_id are the columns update_review() actually
        # revalidates; self.place/self.user are available via backref
        # but are not the source of truth for validation.
        if not self.place_id:
            raise ValueError("place_id is required")
        if not self.user_id:
            raise ValueError("user_id is required")

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
