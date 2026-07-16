import unittest
from app import create_app

class TestHBnBAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    # --- User tests ---
    def test_create_user_success(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
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
            "longitude": -90.0
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "price": 50.0,
            "latitude": 120.0,  # Out of range (-90 to 90)
            "longitude": -90.0
        })
        self.assertEqual(response.status_code, 400)

    # --- Review tests ---
    def test_create_review_empty_text(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 5,
            "user_id": "some-user-id",
            "place_id": "some-place-id"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_rating(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 6,  # Out of range (1 to 5)
            "user_id": "some-user-id",
            "place_id": "some-place-id"
        })
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()