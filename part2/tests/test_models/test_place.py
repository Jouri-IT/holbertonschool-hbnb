#!/usr/bin/python3

import unittest

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.models.base_model import BaseModel


class TestPlace(unittest.TestCase):
    """Unit tests for the Place model."""

    def setUp(self):
        self.owner = User(first_name="Alice", last_name="Smith",
                          email="alice.smith@example.com")

    def test_valid_place_creation(self):
        place = Place(title="Cozy Apartment", description="Nice place",
                      price=100.0, latitude=37.7749, longitude=-122.4194,
                      owner=self.owner)
        self.assertEqual(place.title, "Cozy Apartment")
        self.assertEqual(place.price, 100.0)
        self.assertEqual(place.owner, self.owner)
        self.assertEqual(place.reviews, [])
        self.assertEqual(place.amenities, [])

    def test_place_is_a_base_model(self):
        place = Place(title="Cozy Apartment", price=100.0, latitude=0.0,
                      longitude=0.0, owner=self.owner)
        self.assertIsInstance(place, BaseModel)

    def test_owner_must_be_a_user(self):
        with self.assertRaises(TypeError):
            Place(title="Cozy Apartment", price=100.0, latitude=0.0,
                  longitude=0.0, owner="not-a-user")

    def test_empty_title_rejected(self):
        with self.assertRaises(ValueError):
            Place(title="", price=100.0, latitude=0.0, longitude=0.0,
                  owner=self.owner)

    def test_zero_price_rejected(self):
        with self.assertRaises(ValueError):
            Place(title="Cozy Apartment", price=0, latitude=0.0,
                  longitude=0.0, owner=self.owner)

    def test_negative_price_rejected(self):
        with self.assertRaises(ValueError):
            Place(title="Cozy Apartment", price=-10.0, latitude=0.0,
                  longitude=0.0, owner=self.owner)

    def test_latitude_out_of_range_rejected(self):
        with self.assertRaises(ValueError):
            Place(title="Cozy Apartment", price=100.0, latitude=95.0,
                  longitude=0.0, owner=self.owner)

    def test_longitude_out_of_range_rejected(self):
        with self.assertRaises(ValueError):
            Place(title="Cozy Apartment", price=100.0, latitude=0.0,
                  longitude=200.0, owner=self.owner)

    def test_add_review(self):
        place = Place(title="Cozy Apartment", price=100.0, latitude=0.0,
                      longitude=0.0, owner=self.owner)
        review = Review(text="Great stay!", rating=5, place=place,
                        user=self.owner)
        place.add_review(review)
        self.assertEqual(len(place.reviews), 1)
        self.assertEqual(place.reviews[0].text, "Great stay!")

    def test_add_review_rejects_non_review(self):
        place = Place(title="Cozy Apartment", price=100.0, latitude=0.0,
                      longitude=0.0, owner=self.owner)
        with self.assertRaises(TypeError):
            place.add_review("not-a-review")

    def test_add_review_does_not_duplicate(self):
        place = Place(title="Cozy Apartment", price=100.0, latitude=0.0,
                      longitude=0.0, owner=self.owner)
        review = Review(text="Great stay!", rating=5, place=place,
                        user=self.owner)
        place.add_review(review)
        place.add_review(review)
        self.assertEqual(len(place.reviews), 1)

    def test_add_amenity(self):
        place = Place(title="Cozy Apartment", price=100.0, latitude=0.0,
                      longitude=0.0, owner=self.owner)
        amenity = Amenity(name="Wi-Fi")
        place.add_amenity(amenity)
        self.assertEqual(len(place.amenities), 1)
        self.assertEqual(place.amenities[0].name, "Wi-Fi")

    def test_add_amenity_rejects_non_amenity(self):
        place = Place(title="Cozy Apartment", price=100.0, latitude=0.0,
                      longitude=0.0, owner=self.owner)
        with self.assertRaises(TypeError):
            place.add_amenity("not-an-amenity")

    def test_add_amenity_does_not_duplicate(self):
        place = Place(title="Cozy Apartment", price=100.0, latitude=0.0,
                      longitude=0.0, owner=self.owner)
        amenity = Amenity(name="Wi-Fi")
        place.add_amenity(amenity)
        place.add_amenity(amenity)
        self.assertEqual(len(place.amenities), 1)

    def test_to_dict_flattens_owner_and_relationships(self):
        place = Place(title="Cozy Apartment", price=100.0, latitude=0.0,
                      longitude=0.0, owner=self.owner)
        review = Review(text="Great stay!", rating=5, place=place,
                        user=self.owner)
        amenity = Amenity(name="Wi-Fi")
        place.add_review(review)
        place.add_amenity(amenity)

        data = place.to_dict()
        self.assertNotIn("owner", data)
        self.assertEqual(data["owner_id"], self.owner.id)
        self.assertEqual(data["reviews"], [review.id])
        self.assertEqual(data["amenities"], [amenity.id])


if __name__ == "__main__":
    unittest.main()
