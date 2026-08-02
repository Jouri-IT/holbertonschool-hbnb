#!/usr/bin/python3

import unittest

from app.services.facade import HBnBFacade


class TestFacadeUserEmailUniqueness(unittest.TestCase):
    """Unit tests for email-uniqueness enforcement in HBnBFacade."""

    def setUp(self):
        self.facade = HBnBFacade()

    def test_create_user_rejects_duplicate_email(self):
        self.facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
        })
        with self.assertRaises(ValueError):
            self.facade.create_user({
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "john.doe@example.com",
            })

    def test_update_user_rejects_email_already_taken(self):
        self.facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
        })
        jane = self.facade.create_user({
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
        })
        with self.assertRaises(ValueError):
            self.facade.update_user(jane.id, {"email": "john.doe@example.com"})

    def test_update_user_allows_keeping_own_email(self):
        john = self.facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
        })
        updated = self.facade.update_user(john.id, {
            "email": "john.doe@example.com",
            "first_name": "Jonathan",
        })
        self.assertEqual(updated.first_name, "Jonathan")


if __name__ == "__main__":
    unittest.main()
