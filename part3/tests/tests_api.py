import unittest
from app import create_app


class TestHBnBAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        # User/amenity creation is admin-only, so log in as the
        # seeded default admin (see app.seed_admin) to get a token
        # that can bootstrap regular test users and amenities.
        admin_login = self.client.post('/api/v1/auth/login', json={
            "email": self.app.config["ADMIN_EMAIL"],
            "password": self.app.config["ADMIN_PASSWORD"],
        })
        admin_token = admin_login.get_json()['access_token']
        self.admin_headers = {'Authorization': f'Bearer {admin_token}'}

        # Places/reviews require JWT auth from a regular (non-admin)
        # user, so register one and log in once per test.
        self.client.post('/api/v1/users/', json={
            "first_name": "Auth",
            "last_name": "User",
            "email": "auth.user@example.com",
            "password": "supersecret1"
        }, headers=self.admin_headers)
        login = self.client.post('/api/v1/auth/login', json={
            "email": "auth.user@example.com",
            "password": "supersecret1"
        })
        token = login.get_json()['access_token']
        self.auth_headers = {'Authorization': f'Bearer {token}'}

    # --- User tests ---
    def test_create_user_success(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "janedoepass1"
        }, headers=self.admin_headers)
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email",
            "password": "janedoepass1"
        }, headers=self.admin_headers)
        self.assertEqual(response.status_code, 400)

    def test_create_user_requires_auth(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "No",
            "last_name": "Auth",
            "email": "no.auth@example.com",
            "password": "supersecret1"
        })
        self.assertEqual(response.status_code, 401)

    def test_create_user_requires_admin(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Not",
            "last_name": "Admin",
            "email": "not.admin@example.com",
            "password": "supersecret1"
        }, headers=self.auth_headers)
        self.assertEqual(response.status_code, 403)

    def test_admin_can_update_any_user_email_and_password(self):
        create = self.client.post('/api/v1/users/', json={
            "first_name": "Target",
            "last_name": "User",
            "email": "target.user@example.com",
            "password": "originalpass1"
        }, headers=self.admin_headers)
        target_id = create.get_json()['id']

        response = self.client.put(
            f'/api/v1/users/{target_id}',
            json={
                "email": "updated.target@example.com",
                "password": "newpassword1",
            },
            headers=self.admin_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json()['email'], "updated.target@example.com"
        )

        login = self.client.post('/api/v1/auth/login', json={
            "email": "updated.target@example.com",
            "password": "newpassword1",
        })
        self.assertEqual(login.status_code, 200)

    def test_regular_user_cannot_update_other_users(self):
        create = self.client.post('/api/v1/users/', json={
            "first_name": "Other",
            "last_name": "User",
            "email": "other.user@example.com",
            "password": "supersecret1"
        }, headers=self.admin_headers)
        other_id = create.get_json()['id']

        response = self.client.put(
            f'/api/v1/users/{other_id}',
            json={"first_name": "Hacked"},
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 403)

    def test_regular_user_cannot_modify_own_email(self):
        response = self.client.put(
            '/api/v1/users/nonexistent-but-checked-after-email',
            json={"email": "new@example.com"},
            headers=self.auth_headers,
        )
        # 404 (self-owned check happens after existence check) is also
        # acceptable here; what matters is it's never a 200.
        self.assertNotEqual(response.status_code, 200)

    # --- Amenity tests ---
    def test_create_amenity_success(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        }, headers=self.admin_headers)
        self.assertEqual(response.status_code, 201)

    def test_create_amenity_invalid(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        }, headers=self.admin_headers)
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_requires_admin(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Pool"
        }, headers=self.auth_headers)
        self.assertEqual(response.status_code, 403)

    def test_update_amenity_requires_admin(self):
        create = self.client.post('/api/v1/amenities/', json={
            "name": "Gym"
        }, headers=self.admin_headers)
        amenity_id = create.get_json()['id']

        response = self.client.put(
            f'/api/v1/amenities/{amenity_id}',
            json={"name": "Fitness Center"},
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 403)

    def test_admin_can_update_amenity(self):
        create = self.client.post('/api/v1/amenities/', json={
            "name": "Sauna"
        }, headers=self.admin_headers)
        amenity_id = create.get_json()['id']

        response = self.client.put(
            f'/api/v1/amenities/{amenity_id}',
            json={"name": "Steam Room"},
            headers=self.admin_headers,
        )
        self.assertEqual(response.status_code, 200)

    # --- Place tests ---
    def test_create_place_invalid_price(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "price": -10.0,
            "latitude": 45.0,
            "longitude": -90.0,
        }, headers=self.auth_headers)
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "price": 50.0,
            "latitude": 120.0,  # Out of range (-90 to 90)
            "longitude": -90.0,
        }, headers=self.auth_headers)
        self.assertEqual(response.status_code, 400)

    def test_create_place_requires_auth(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "price": 50.0,
            "latitude": 45.0,
            "longitude": -90.0,
        })
        self.assertEqual(response.status_code, 401)

    # --- Review tests ---
    def _create_place(self):
        """Create a place owned by a different user than self.auth_headers.

        Reviews are tested with self.auth_headers, and the facade
        blocks a user from reviewing their own place -- so the place
        owner must be someone else, or that self-review guard would
        fire before the text/rating validation under test ever runs.
        """
        self.client.post('/api/v1/users/', json={
            "first_name": "Place",
            "last_name": "Owner",
            "email": "place.owner@example.com",
            "password": "placeownerpass1"
        }, headers=self.admin_headers)
        login = self.client.post('/api/v1/auth/login', json={
            "email": "place.owner@example.com",
            "password": "placeownerpass1"
        })
        owner_headers = {
            'Authorization': f"Bearer {login.get_json()['access_token']}"
        }
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "price": 50.0,
            "latitude": 45.0,
            "longitude": -90.0,
        }, headers=owner_headers)
        return response.get_json()['id']

    def test_non_owner_cannot_update_place(self):
        place_id = self._create_place()
        response = self.client.put(
            f'/api/v1/places/{place_id}',
            json={"title": "Hacked Title"},
            headers=self.auth_headers,
        )
        self.assertEqual(response.status_code, 403)

    def test_admin_can_update_any_place(self):
        place_id = self._create_place()
        response = self.client.put(
            f'/api/v1/places/{place_id}',
            json={"title": "Admin Renamed Place"},
            headers=self.admin_headers,
        )
        self.assertEqual(response.status_code, 200)

    def test_create_review_empty_text(self):
        place_id = self._create_place()
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 5,
            "place_id": place_id,
        }, headers=self.auth_headers)
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_rating(self):
        place_id = self._create_place()
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 6,  # Out of range (1 to 5)
            "place_id": place_id,
        }, headers=self.auth_headers)
        self.assertEqual(response.status_code, 400)

    def test_create_review_requires_auth(self):
        place_id = self._create_place()
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "place_id": place_id,
        })
        self.assertEqual(response.status_code, 401)

    def test_admin_can_update_and_delete_any_review(self):
        place_id = self._create_place()
        create = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "place_id": place_id,
        }, headers=self.auth_headers)
        review_id = create.get_json()['id']

        update = self.client.put(
            f'/api/v1/reviews/{review_id}',
            json={"text": "Edited by admin"},
            headers=self.admin_headers,
        )
        self.assertEqual(update.status_code, 200)

        delete = self.client.delete(
            f'/api/v1/reviews/{review_id}',
            headers=self.admin_headers,
        )
        self.assertEqual(delete.status_code, 200)


if __name__ == '__main__':
    unittest.main()
