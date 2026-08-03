#!/usr/bin/python3

import re
import uuid
from app import db, bcrypt
from app.models.base_model import BaseModel


class User(BaseModel):
    """User model.

    Attributes:
        first_name
        last_name
        email
        password
        is_admin
    """

    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password,
                 is_admin=False):
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        self.password = ""
        self.hash_password(password)

        self.validate()

    def hash_password(self, password):
        """Hash the password before storing it."""
        if not isinstance(password, str) or not password:
            raise TypeError("password must be a non-empty string")

        self.password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

    def verify_password(self, password):
        """Verify the password."""
        return bcrypt.check_password_hash(
            self.password,
            password
        )

    def validate(self):
        """Validate user attributes."""

        if not isinstance(self.first_name, str):
            raise TypeError("first_name must be a string")
        if len(self.first_name) == 0 or len(self.first_name) > 50:
            raise ValueError("Invalid first_name")

        if not isinstance(self.last_name, str):
            raise TypeError("last_name must be a string")
        if len(self.last_name) == 0 or len(self.last_name) > 50:
            raise ValueError("Invalid last_name")

        if not isinstance(self.email, str):
            raise TypeError("email must be a string")

        email_pattern = r"^[^@]+@[^@]+\.[^@]+$"
        if not re.match(email_pattern, self.email):
            raise ValueError("Invalid email")

        if not isinstance(self.is_admin, bool):
            raise TypeError("is_admin must be boolean")

    def to_dict(self):
        """Return dictionary representation without password."""
        data = super().to_dict()
        data.pop("password", None)
        return data
