#!/usr/bin/python3

from app import db
from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity


class Place(BaseModel):
    """Place model."""

    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # Plain scalar copy of the owner's id -- a real db.ForeignKey and
    # relationship() land in the relationships task, not this one.
    # It's still a mapped column (not just a Python attribute) so
    # ownership survives across requests/sessions; `owner` below is
    # a same-request-only convenience reference to the actual User.
    owner_id = db.Column(db.String(36), nullable=False)

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

        # self.owner (the actual User object) is only ever set at
        # construction time and doesn't survive a fresh DB fetch in a
        # later request (no relationship() yet) -- owner_id, a real
        # column, does, and is what update_place() actually revalidates.
        if not self.owner_id:
            raise ValueError("owner_id is required")

    def add_review(self, review):
        """Add review to place, skipping it if already attached."""
        # Imported locally to avoid a circular import: review.py
        # already imports Place at module load time.
        from app.models.review import Review
        if not isinstance(review, Review):
            raise TypeError("review must be a Review")
        # A place fetched fresh from the DB (rather than freshly
        # constructed) won't have `reviews` set yet -- see the
        # to_dict() note below.
        if not hasattr(self, 'reviews'):
            self.reviews = []
        if not any(r.id == review.id for r in self.reviews):
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add amenity to place, skipping it if already attached."""
        if not isinstance(amenity, Amenity):
            raise TypeError("amenity must be an Amenity")
        if not hasattr(self, 'amenities'):
            self.amenities = []
        if not any(a.id == amenity.id for a in self.amenities):
            self.amenities.append(amenity)

    def to_dict(self):
        """Return dictionary representation with flattened relationships."""
        data = super().to_dict()
        data.pop("owner", None)
        data["owner_id"] = self.owner_id
        # reviews/amenities are plain (unmapped) attributes only ever
        # set at construction time -- a Place fetched fresh from the
        # DB in a later request won't have them, since there's no
        # relationship() to reload them from yet.
        data["reviews"] = [review.id for review in getattr(self, 'reviews', [])]
        data["amenities"] = [amenity.id for amenity in getattr(self, 'amenities', [])]
        return data
