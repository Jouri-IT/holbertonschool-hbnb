#!/usr/bin/python3

import unittest

from app.models.user import User
from app.models.base_model import BaseModel


class TestUser(unittest.TestCase):
    """Unit tests for the User model."""

    def test_valid_user_creation(self):
        user = User(first_name="John", last_name="Doe",
                    email="john.doe@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertFalse(user.is_admin)

    def test_user_is_a_base_model(self):
        user = User(first_name="John", last_name="Doe",
                    email="john.doe@example.com")
        self.assertIsInstance(user, BaseModel)

    def test_is_admin_can_be_set_true(self):
        user = User(first_name="Ada", last_name="Lovelace",
                    email="ada@example.com", is_admin=True)
        self.assertTrue(user.is_admin)

    def test_empty_first_name_rejected(self):
        with self.assertRaises(ValueError):
            User(first_name="", last_name="Doe", email="a@example.com")

    def test_first_name_too_long_rejected(self):
        with self.assertRaises(ValueError):
            User(first_name="a" * 51, last_name="Doe",
                 email="a@example.com")

    def test_empty_last_name_rejected(self):
        with self.assertRaises(ValueError):
            User(first_name="John", last_name="", email="a@example.com")

    def test_last_name_too_long_rejected(self):
        with self.assertRaises(ValueError):
            User(first_name="John", last_name="a" * 51,
                 email="a@example.com")

    def test_invalid_email_format_rejected(self):
        with self.assertRaises(ValueError):
            User(first_name="John", last_name="Doe", email="not-an-email")

    def test_non_string_is_admin_rejected(self):
        with self.assertRaises(TypeError):
            User(first_name="John", last_name="Doe",
                 email="a@example.com", is_admin="yes")

    def test_password_excluded_from_to_dict(self):
        user = User(first_name="John", last_name="Doe",
                    email="john.doe@example.com", password="secret123")
        self.assertNotIn("password", user.to_dict())


if __name__ == "__main__":
    unittest.main()
