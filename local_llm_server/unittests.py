import unittest
from fastapi.testclient import TestClient

from app import app

class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_generate_response(self):
        payload = {
            "prompt": "Hello",
            "max_tokens": 50
        }
        response = self.client.post("/generate", json=payload)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("response", data)
        self.assertIsInstance(data["response"], str)

if __name__ == "__main__":
    unittest.main()
