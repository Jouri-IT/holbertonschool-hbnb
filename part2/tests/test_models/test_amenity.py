#!/usr/bin/python3

import unittest

from app.models.amenity import Amenity
from app.models.base_model import BaseModel


class TestAmenity(unittest.TestCase):
    """Unit tests for the Amenity model."""

    def test_valid_amenity_creation(self):
        amenity = Amenity(name="Wi-Fi")
        self.assertEqual(amenity.name, "Wi-Fi")

    def test_amenity_is_a_base_model(self):
        amenity = Amenity(name="Wi-Fi")
        self.assertIsInstance(amenity, BaseModel)

    def test_empty_name_rejected(self):
        with self.assertRaises(ValueError):
            Amenity(name="")

    def test_name_too_long_rejected(self):
        with self.assertRaises(ValueError):
            Amenity(name="a" * 51)

    def test_non_string_name_rejected(self):
        with self.assertRaises(TypeError):
            Amenity(name=123)

    def test_list_amenities_returns_plain_list(self):
        a1 = Amenity(name="Wi-Fi")
        a2 = Amenity(name="Pool")
        result = Amenity.list_amenities([a1, a2])
        self.assertEqual(result, [a1, a2])


if __name__ == "__main__":
    unittest.main()
