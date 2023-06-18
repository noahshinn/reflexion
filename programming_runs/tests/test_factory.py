import unittest
from unittest import mock

from generators.factory import generator_factory, llm_factory
from generators.local_request import LocalRequest
from generators.openai_request import OpenAIRequest
from generators.py_generate import PyGenerator
from generators.rs_generate import RsGenerator
from generators.api_endpoint import endpoint


class GeneratorsFactoryTests(unittest.TestCase):
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
        endpoint.set_api_endpoint("http://127.0.0.1:8081/generate")
        llm_request = llm_factory()
        self.assertIsInstance(llm_request, LocalRequest)

    def test_llm_factory_with_openai_endpoint(self):
        # Test llm_factory with OpenAI endpoint
        endpoint.set_api_endpoint(None)
        llm_request = llm_factory()
        self.assertIsInstance(llm_request, OpenAIRequest)


if __name__ == "__main__":
    unittest.main()
