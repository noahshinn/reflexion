import unittest
import responses
from your_module import LocalRequest

class TestLocalRequest(unittest.TestCase):
    def setUp(self):
        self.url = "http://example.com"  # Replace with the actual URL
        self.local_request = LocalRequest(self.url)

    @responses.activate
    def test_completion_successful(self):
        # Mock the response for the completion request
        mock_response = {"your_field_here": "mocked_completion_response"}
        responses.add(responses.GET, self.url, json=mock_response, status=200)

        # Call the completion method
        model = "model_name"
        prompt = "prompt_text"
        max_tokens = 1024
        stop_strs = None
        temperature = 0.0
        num_comps = 1
        result = self.local_request.completion(model, prompt, max_tokens, stop_strs, temperature, num_comps)

        # Assert the mock function calls and the result
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, self.url)
        params = responses.calls[0].request.params
        self.assertEqual(params['model'], model)
        self.assertEqual(params['prompt'], prompt)
        self.assertEqual(params['max_tokens'], str(max_tokens))
        self.assertEqual(params['stop_strs'], stop_strs)
        self.assertEqual(params['temperature'], str(temperature))
        self.assertEqual(params['num_comps'], str(num_comps))
        self.assertEqual(result, "mocked_completion_response")

    @responses.activate
    def test_completion_failed(self):
        # Mock the response for the completion request
        responses.add(responses.GET, self.url, status=400)

        # Call the completion method
        model = "model_name"
        prompt = "prompt_text"
        result = self.local_request.completion(model, prompt)

        # Assert the mock function calls and the result
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, self.url)
        self.assertIsNone(result)

    def test_chat(self):
        # Mock the completion method
        with unittest.mock.patch.object(self.local_request, "completion") as mock_completion:
            # Set up the mock return value
            mock_completion.return_value = "mocked_chat_response"

            # Call the chat method
            model = "model_name"
            system_message = "system_message"
            user_message = "user_message"
            max_tokens = 1024
            temperature = 0.0
            num_comps = 1
            result = self.local_request.chat(model, system_message, user_message, max_tokens, temperature, num_comps)

            # Assert the mock function calls and the result
            mock_completion.assert_called_once_with(model, f"{system_message} \n{user_message}", max_tokens, temperature, num_comps)
            self.assertEqual(result, "mocked_chat_response")

if __name__ == "__main__":
    unittest.main()
