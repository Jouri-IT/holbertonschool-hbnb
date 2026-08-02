import unittest
from app import create_app


class TestHBnBAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        # Places/reviews now require JWT auth, so register a user and
        # log in once per test to get a token for those requests.
        self.client.post('/api/v1/users/', json={
            "first_name": "Auth",
            "last_name": "User",
            "email": "auth.user@example.com",
            "password": "supersecret1"
        })
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
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email",
            "password": "janedoepass1"
        })
        self.assertEqual(response.status_code, 400)

    # --- Amenity tests ---
    def test_create_amenity_success(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_amenity_invalid(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)

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
        })
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


if __name__ == '__main__':
    unittest.main()
