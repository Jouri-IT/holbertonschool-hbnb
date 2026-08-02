#!/usr/bin/python3

import unittest

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.base_model import BaseModel


class TestReview(unittest.TestCase):
    """Unit tests for the Review model."""

    def setUp(self):
        self.owner = User(first_name="Alice", last_name="Smith",
                          email="alice.smith@example.com")
        self.place = Place(title="Cozy Apartment", price=100.0,
                           latitude=0.0, longitude=0.0, owner=self.owner)

    def test_valid_review_creation(self):
        review = Review(text="Great stay!", rating=5, place=self.place,
                        user=self.owner)
        self.assertEqual(review.text, "Great stay!")
        self.assertEqual(review.rating, 5)

    def test_review_is_a_base_model(self):
        review = Review(text="Great stay!", rating=5, place=self.place,
                        user=self.owner)
        self.assertIsInstance(review, BaseModel)

    def test_review_keeps_place_and_user_object_references(self):
        review = Review(text="Great stay!", rating=5, place=self.place,
                        user=self.owner)
        self.assertIs(review.place, self.place)
        self.assertIs(review.user, self.owner)

    def test_place_id_and_user_id_derived_from_objects(self):
        review = Review(text="Great stay!", rating=5, place=self.place,
                        user=self.owner)
        self.assertEqual(review.place_id, self.place.id)
        self.assertEqual(review.user_id, self.owner.id)

    def test_place_must_be_a_place_instance(self):
        with self.assertRaises(TypeError):
            Review(text="Great stay!", rating=5, place="not-a-place",
                   user=self.owner)

    def test_user_must_be_a_user_instance(self):
        with self.assertRaises(TypeError):
            Review(text="Great stay!", rating=5, place=self.place,
                   user="not-a-user")

    def test_empty_text_rejected(self):
        with self.assertRaises(ValueError):
            Review(text="", rating=5, place=self.place, user=self.owner)

    def test_rating_out_of_range_rejected(self):
        with self.assertRaises(ValueError):
            Review(text="Great stay!", rating=6, place=self.place,
                   user=self.owner)
        with self.assertRaises(ValueError):
            Review(text="Great stay!", rating=0, place=self.place,
                   user=self.owner)

    def test_boolean_rating_rejected(self):
        with self.assertRaises(TypeError):
            Review(text="Great stay!", rating=True, place=self.place,
                   user=self.owner)

    def test_to_dict_flattens_place_and_user(self):
        review = Review(text="Great stay!", rating=5, place=self.place,
                        user=self.owner)
        data = review.to_dict()
        self.assertNotIn("place", data)
        self.assertNotIn("user", data)
        self.assertEqual(data["place_id"], self.place.id)
        self.assertEqual(data["user_id"], self.owner.id)

    def test_list_by_place(self):
        other_place = Place(title="Other Place", price=50.0, latitude=0.0,
                            longitude=0.0, owner=self.owner)
        review1 = Review(text="Great stay!", rating=5, place=self.place,
                         user=self.owner)
        review2 = Review(text="Meh", rating=3, place=other_place,
                         user=self.owner)
        result = Review.list_by_place([review1, review2], self.place.id)
        self.assertEqual(result, [review1])


if __name__ == "__main__":
    unittest.main()
