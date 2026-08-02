#!/usr/bin/python3

import unittest
from time import sleep

from app.models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Unit tests for the shared BaseModel behavior."""

    def test_id_is_a_string_uuid(self):
        obj = BaseModel()
        self.assertIsInstance(obj.id, str)
        self.assertTrue(len(obj.id) > 0)

    def test_ids_are_unique(self):
        obj1 = BaseModel()
        obj2 = BaseModel()
        self.assertNotEqual(obj1.id, obj2.id)

    def test_created_at_and_updated_at_set_on_creation(self):
        obj = BaseModel()
        self.assertIsNotNone(obj.created_at)
        self.assertIsNotNone(obj.updated_at)

    def test_save_updates_updated_at(self):
        obj = BaseModel()
        original_updated_at = obj.updated_at
        sleep(0.01)
        obj.save()
        self.assertGreater(obj.updated_at, original_updated_at)
        self.assertNotEqual(obj.created_at, obj.updated_at)

    def test_update_sets_attributes_and_bumps_updated_at(self):
        obj = BaseModel()
        obj.name = "before"
        original_updated_at = obj.updated_at
        sleep(0.01)
        obj.update({"name": "after"})
        self.assertEqual(obj.name, "after")
        self.assertGreater(obj.updated_at, original_updated_at)

    def test_update_protects_id_created_at_updated_at(self):
        obj = BaseModel()
        original_id = obj.id
        original_created_at = obj.created_at
        obj.update({"id": "hacked", "created_at": "hacked"})
        self.assertEqual(obj.id, original_id)
        self.assertEqual(obj.created_at, original_created_at)

    def test_update_ignores_unknown_attributes(self):
        obj = BaseModel()
        obj.update({"does_not_exist": "value"})
        self.assertFalse(hasattr(obj, "does_not_exist"))

    def test_update_rolls_back_on_validation_failure(self):
        obj = BaseModel()
        obj.name = "valid"

        def validate():
            if obj.name == "invalid":
                raise ValueError("bad name")

        obj.validate = validate
        with self.assertRaises(ValueError):
            obj.update({"name": "invalid"})
        self.assertEqual(obj.name, "valid")

    def test_to_dict_serializes_datetimes(self):
        obj = BaseModel()
        data = obj.to_dict()
        self.assertIsInstance(data["created_at"], str)
        self.assertIsInstance(data["updated_at"], str)


if __name__ == "__main__":
    unittest.main()
