import unittest
import time
import os

from fastapi.testclient import TestClient

from ..app.utils import generate_uid
from ..app.main import app
from ..app.utils import get_api_keys


class APITests(unittest.TestCase):
    def _get_api_key(self) -> str:
        api_keys_path = os.environ["API_KEYS_PATH"]
        valid_api_keys = get_api_keys(api_keys_path=api_keys_path)
        return valid_api_keys[0]


    def setUp(self):
        self.client = TestClient(app)
        self.api_key: str = self._get_api_key()
        self.uid: str = generate_uid()
        self.headers = {  
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        # Additional setup for your tests

    def test_process_data(self):
        # Define a test case for the `/process/` endpoint
        response = self.client.post(
            "/process/",
            json={
                "start": "start_value", "stop": "stop_value", "id": 1, 
                "process_uid": self.uid
            },
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        content: dict = response.json()
        self.assertIn("uid", content.keys())
        self.assertIn("url", content.keys())

    def test_get_status(self):
        # Define a test case for the `/status/` endpoint
        time.sleep(5)
        response = self.client.get(
            f"/status/{self.uid}",
            headers=self.headers
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
