#!/usr/bin/python3

import uuid
from datetime import datetime


class BaseModel:
    """Base class for all models."""

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update updated_at timestamp."""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update object attributes."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """Return dictionary representation."""
        return self.__dict__
