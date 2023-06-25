import unittest
from unittest import mock

from programming_runs.generators.local_llm_config import APIEndPoint


class TestAPIEndPoint(unittest.TestCase):
    def setUp(self):
        self.endpoint = APIEndPoint()

    def test_set_api_endpoint(self):
        endpoint_value = "http://example.com/api"
        
        self.endpoint.set_api_endpoint(endpoint_value)
        api_endpoint = self.endpoint.get_api_endpoint()

        self.assertEqual(api_endpoint, endpoint_value)

    def test_get_api_endpoint(self):
        # Set up a mock object for the external function call
        with mock.patch("your_module.external_function") as mock_external_function:
            mock_external_function.return_value = "http://example.com/api"

            api_endpoint = self.endpoint.get_api_endpoint()

            mock_external_function.assert_called_once()
            self.assertEqual(api_endpoint, "http://example.com/api")

if __name__ == "__main__":
    unittest.main()
