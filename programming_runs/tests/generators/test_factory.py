import unittest
from unittest import mock

from programming_runs.generators.factory import generator_factory, llm_factory
from programming_runs.generators.local_request import LocalRequest
from programming_runs.generators.openai_request import OpenAIRequest
from programming_runs.generators.py_generate import PyGenerator
from programming_runs.generators.rs_generate import RsGenerator

class MyModuleTests(unittest.TestCase):
    def test_generator_factory_with_python_language(self):
        # Test generator_factory with python language
        generator = generator_factory("python")
        self.assertIsInstance(generator, PyGenerator)

    def test_generator_factory_with_rust_language(self):
        # Test generator_factory with rust language
        generator = generator_factory("rust")
        self.assertIsInstance(generator, RsGenerator)

    def test_generator_factory_with_invalid_language(self):
        # Test generator_factory with invalid language
        with self.assertRaises(ValueError):
            generator_factory("invalid")

    def test_llm_factory_with_local_endpoint(self):
        # Test llm_factory with local endpoint
        with mock.patch("mymodule.endpoint") as mock_endpoint:
            mock_endpoint.get_api_endpoint.return_value = "http://127.0.0.1:8081/generate"
            llm_request = llm_factory()
        self.assertIsInstance(llm_request, LocalRequest)

    def test_llm_factory_with_openai_endpoint(self):
        # Test llm_factory with OpenAI endpoint
        with mock.patch("mymodule.endpoint") as mock_endpoint:
            mock_endpoint.get_api_endpoint.return_value = None
            llm_request = llm_factory()
        self.assertIsInstance(llm_request, OpenAIRequest)


if __name__ == "__main__":
    unittest.main()