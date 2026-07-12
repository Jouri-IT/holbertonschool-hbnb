#!/usr/bin/python3

import uuid
from datetime import datetime


class BaseModel:
    """Base class for all models.

    Provides the shared id/timestamp fields and the create(), update(),
    delete() lifecycle hooks from the Part 1 class diagram. Actual
    persistence (INSERT/UPDATE/DELETE) is the Persistence layer's job,
    per our own architecture doc -- these hooks keep the object itself
    internally consistent (timestamps, validation) regardless of how
    it's stored.
    """

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def create(self):
        """Lifecycle hook for when the object is first persisted."""
        self.save()

    def save(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update attributes from a dict, then re-validate.

        id/created_at/updated_at are protected from being overwritten
        by a caller. If the subclass defines validate(), it's run
        after the update so a bad update can never leave the object
        in an invalid state (this was previously missing). The update
        is transactional: if validation fails, all changed attributes
        are rolled back so the object is never left half-applied.
        """
        protected = ("id", "created_at", "updated_at")
        previous = {}

        for key, value in data.items():
            if hasattr(self, key) and key not in protected:
                previous[key] = getattr(self, key)
                setattr(self, key, value)

        if hasattr(self, "validate"):
            try:
                self.validate()
            except (TypeError, ValueError):
                for key, old_value in previous.items():
                    setattr(self, key, old_value)
                raise

        self.save()

    def delete(self):
        """Lifecycle hook for when the object is removed."""
        pass

    def to_dict(self):
        """Return a JSON-serializable dictionary representation."""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result
