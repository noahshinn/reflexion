import unittest
from unittest import mock
from mymodule import (
    generic_generate_func_impl,
    generic_generate_internal_tests,
    generic_generate_self_reflection,
    completion,
    chat,
    sample_n_random,
)

class GeneratorFactoryTests(unittest.TestCase):

    def test_generic_generate_func_impl_gpt4_reflexion_chat(self):
        with mock.patch("mymodule.chat") as mock_chat:
            func_sig = "..."
            model = "gpt-4"
            strategy = "reflexion"
            prev_func_impl = "..."
            feedback = "..."
            self_reflection = "..."
            num_comps = 1
            temperature = 0.0
            REFLEXION_CHAT_INSTRUCTION = "..."
            REFLEXION_FEW_SHOT = "..."

            mock_chat.return_value = "mocked_chat_response"

            result = generic_generate_func_impl(
                func_sig,
                model,
                strategy,
                prev_func_impl,
                feedback,
                self_reflection,
                num_comps,
                temperature,
                REFLEXION_CHAT_INSTRUCTION,
                REFLEXION_FEW_SHOT,
                None,
                None,
                None,
                None
            )

            mock_chat.assert_called_once_with(
                model,
                REFLEXION_CHAT_INSTRUCTION,
                f"{REFLEXION_FEW_SHOT}\n[previous impl]:\n{prev_func_impl}\n\n[unit test results from previous impl]:\n{feedback}\n\n[reflection on previous impl]:\n{self_reflection}\n\n[improved impl]:\n{func_sig}",
                num_comps=num_comps,
                temperature=temperature
            )
            self.assertEqual(result, "mocked_chat_response")




    def test_generic_generate_func_impl_gpt4_simple_chat(self):
        with mock.patch("mymodule.chat") as mock_chat:
            func_sig = "..."
            model = "gpt-4"
            strategy = "simple"
            prev_func_impl = "..."
            feedback = "..."
            self_reflection = "..."
            num_comps = 1
            temperature = 0.0
            SIMPLE_CHAT_INSTRUCTION = "..."

            mock_chat.return_value = "mocked_chat_response"

            result = generic_generate_func_impl(
                func_sig,
                model,
                strategy,
                prev_func_impl,
                feedback,
                self_reflection,
                num_comps,
                temperature,
                None,
                None,
                SIMPLE_CHAT_INSTRUCTION,
                None,
                None,
                None
            )

            mock_chat.assert_called_once_with(
                model,
                SIMPLE_CHAT_INSTRUCTION,
                func_sig,
                num_comps=num_comps,
                temperature=temperature
            )
            self.assertEqual(result, "mocked_chat_response")



    def test_generic_generate_func_impl_other_models_reflexion_completion(self):
        with mock.patch("mymodule.completion") as mock_completion:
            func_sig = "..."
            model = "other_model"
            strategy = "reflexion"
            prev_func_impl = "..."
            feedback = "..."
            self_reflection = "..."
            num_comps = 1
            temperature = 0.0
            REFLEXION_COMPLETION_INSTRUCTION = "..."

            mock_completion.return_value = "mocked_completion_response"

            result = generic_generate_func_impl(
                func_sig,
                model,
                strategy,
                prev_func_impl,
                feedback,
                self_reflection,
                num_comps,
                temperature,
                None,
                None,
                None,
                REFLEXION_COMPLETION_INSTRUCTION,
                None,
                None
            )

            mock_completion.assert_called_once_with(
                model,
                f"{REFLEXION_COMPLETION_INSTRUCTION}\n{prev_func_impl}\n\nunit tests:\n{feedback}\n\nhint:\n{self_reflection}\n\n# improved implementation\n{func_sig}",
                num_comps=num_comps,
                temperature=temperature
            )
            self.assertEqual(result, "mocked_completion_response")


    def test_generic_generate_internal_tests(self):
        # Mock necessary dependencies
        with mock.patch("mymodule.chat") as mock_chat, mock.patch("mymodule.completion") as mock_completion:
            func_sig = "..."
            model = "..."
            committee_size = 1
            max_num_tests = 10
            TEST_GENERATION_FEW_SHOT = "..."
            TEST_GENERATION_CHAT_INSTRUCTION = "..."
            TEST_GENERATION_COMPLETION_INSTRUCTION = "..."
            parse_tests = lambda x: [x]
            is_syntax_valid = lambda x: True
            is_react = False

            # Mock the return value of chat and completion functions
            mock_chat.return_value = "mocked_chat_response"
            mock_completion.return_value = "mocked_completion_response"

            result = generic_generate_internal_tests(
                func_sig,
                model,
                committee_size,
                max_num_tests,
                TEST_GENERATION_FEW_SHOT,
                TEST_GENERATION_CHAT_INSTRUCTION,
                TEST_GENERATION_COMPLETION_INSTRUCTION,
                parse_tests,
                is_syntax_valid,
                is_react
            )

            # Assert the result based on expected behavior
            mock_chat.assert_called_once_with(
                model,
                TEST_GENERATION_CHAT_INSTRUCTION,
                f'{TEST_GENERATION_FEW_SHOT}\n\nfunc signature:\n{func_sig}\nunit tests:',
                max_tokens=1024
            )
            self.assertEqual(result, ["mocked_chat_response"])
            mock_completion.assert_not_called()  # Ensure that the completion function is not called
    

    def test_generic_generate_func_impl_other_models_simple_completion(self):
        with mock.patch("mymodule.completion") as mock_completion:
            func_sig = "..."
            model = "other_model"
            strategy = "simple"
            num_comps = 1
            temperature = 0.0
            SIMPLE_COMPLETION_INSTRUCTION = "..."

            mock_completion.return_value = "mocked_completion_response"

            result = generic_generate_func_impl(
                func_sig,
                model,
                strategy,
                None,
                None,
                None,
                num_comps,
                temperature,
                None,
                None,
                None,
                None,
                SIMPLE_COMPLETION_INSTRUCTION,
                None
            )

            mock_completion.assert_called_once_with(
                model,
                f"{SIMPLE_COMPLETION_INSTRUCTION}\n{func_sig}",
                num_comps=num_comps,
                temperature=temperature
            )
            self.assertEqual(result, "mocked_completion_response")


    def test_generic_generate_self_reflection(self):
        # Mock necessary dependencies
        with mock.patch("mymodule.chat") as mock_chat, mock.patch("mymodule.completion") as mock_completion:
            func = "..."
            feedback = "..."
            model = "..."
            SELF_REFLECTION_CHAT_INSTRUCTION = "..."
            SELF_REFLECTION_COMPLETION_INSTRUCTION = "..."
            SELF_REFLECTION_FEW_SHOT = "..."

            # Mock the return value of chat and completion functions
            mock_chat.return_value = "mocked_chat_response"
            mock_completion.return_value = "mocked_completion_response"

            result = generic_generate_self_reflection(
                func,
                feedback,
                model,
                SELF_REFLECTION_CHAT_INSTRUCTION,
                SELF_REFLECTION_COMPLETION_INSTRUCTION,
                SELF_REFLECTION_FEW_SHOT
            )

            # Assert the result based on expected behavior
            mock_chat.assert_called_once_with(
                model,
                SELF_REFLECTION_CHAT_INSTRUCTION,
                f'Function implementation:\n{func}\n\nUnit test results:\n{feedback}\n\nSelf-reflection:',
                max_tokens=1024
            )
            self.assertEqual(result, "mocked_chat_response")

            mock_completion.assert_not_called()  # Ensure that the completion function is not called

def test_completion(self):
    # Mock necessary dependencies
    with mock.patch("mymodule.factory.llm_factory") as mock_llm_factory:
        # Create a mock instance of the llm_factory
        mock_llm_instance = mock.Mock()
        # Mock the return value of llm_factory to return the mock instance
        mock_llm_factory.return_value = mock_llm_instance

        model = "..."
        prompt = "..."
        max_tokens = 1024
        stop_strs = None
        temperature = 0.0
        num_comps = 1

        completion_mock = mock.Mock()
        mock_llm_instance.completion = completion_mock

        completion(model, prompt, max_tokens, stop_strs, temperature, num_comps)

        # Assert the interaction with the mocked dependencies
        mock_llm_factory.assert_called_once()  # Assert that the llm_factory method was called
        completion_mock.assert_called_once_with(  # Assert that the completion method was called with the correct arguments
            model,
            prompt,
            max_tokens,
            stop_strs,
            temperature,
            num_comps
        )


    def test_chat(self):
        # Mock necessary dependencies
        with mock.patch("mymodule.factory.llm_factory") as mock_llm_factory:
            # Create a mock instance of the llm_factory
            mock_llm_instance = mock.Mock()
            # Mock the return value of llm_factory to return the mock instance
            mock_llm_factory.return_value = mock_llm_instance

            # Mock the chat method of the mock_llm_instance
            mock_chat = mock.Mock()
            mock_llm_instance.chat = mock_chat

            model = "..."
            system_message = "..."
            user_message = "..."
            max_tokens = 1024
            temperature = 0.0
            num_comps = 1

            chat(model, system_message, user_message, max_tokens, temperature, num_comps)

            # Assert the interaction with the mocked dependencies
            mock_llm_factory.assert_called_once()  # Assert that the llm_factory method was called
            mock_chat.assert_called_once_with(  # Assert that the chat method was called with the correct arguments
                model,
                system_message,
                user_message,
                max_tokens,
                temperature,
                num_comps
            )


    def test_sample_n_random(self):
        items = ["item1", "item2", "item3"]
        n = 2

        result = sample_n_random(items, n)

        self.assertEqual(len(result), n)  # Assert that the result has the expected length

        for item in result:
            self.assertIn(item, items)  # Assert that each item in the result is from the original list



if __name__ == "__main__":
    unittest.main()
