#!/usr/bin/python3

import re
from app.models.base_model import BaseModel


class User(BaseModel):
    """User model.

    Attributes per Part 1 design: first_name, last_name, email,
    password, is_admin.
    """

    def __init__(self, first_name, last_name, email, password=None,
                 is_admin=False):
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin

        self.validate()

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

        if self.password is not None:
            if not isinstance(self.password, str):
                raise TypeError("password must be a string")
            if len(self.password) < 6:
                raise ValueError("password must be at least 6 characters")

        if not isinstance(self.is_admin, bool):
            raise TypeError("is_admin must be boolean")

    def to_dict(self):
        """Return dictionary representation, excluding the password."""
        data = super().to_dict()
        data.pop("password", None)
        return data
