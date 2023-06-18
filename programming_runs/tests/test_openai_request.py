import unittest
from unittest import mock
from your_module import OpenAIRequest

class TestOpenAIRequest(unittest.TestCase):
    def setUp(self):
        self.openai_request = OpenAIRequest()

    def test_completion_successful(self):
        # Mock the openai.Completion.create function and its response
        with mock.patch.object(self.openai_request.openai_module.Completion, "create") as mock_create:
            # Set up the mock response
            mock_response = mock.Mock()
            mock_response.choices = [mock.Mock(text="mocked_completion_response")]
            mock_create.return_value = mock_response

            # Call the completion method
            model = "model_name"
            prompt = "prompt_text"
            max_tokens = 1024
            stop_strs = None
            temperature = 0.0
            num_comps = 1
            result = self.openai_request.completion(model, prompt, max_tokens, stop_strs, temperature, num_comps)

            # Assert the mock function calls and the result
            mock_create.assert_called_once_with(
                model=model,
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=stop_strs,
                n=num_comps
            )
            self.assertEqual(result, "mocked_completion_response")

    def test_chat_successful(self):
        # Mock the openai.ChatCompletion.create function and its response
        with mock.patch.object(self.openai_request.openai_module.ChatCompletion, "create") as mock_create:
            # Set up the mock response
            mock_response = mock.Mock()
            mock_response.choices = [mock.Mock(message=mock.Mock(content="mocked_chat_response"))]
            mock_create.return_value = mock_response

            # Call the chat method
            model = "model_name"
            system_message = "system_message"
            user_message = "user_message"
            max_tokens = 1024
            temperature = 0.0
            num_comps = 1
            result = self.openai_request.chat(model, system_message, user_message, max_tokens, temperature, num_comps)

            # Assert the mock function calls and the result
            mock_create.assert_called_once_with(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                n=num_comps
            )
            self.assertEqual(result, "mocked_chat_response")

if __name__ == "__main__":
    unittest.main()
