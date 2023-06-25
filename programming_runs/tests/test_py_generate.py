import unittest
from unittest.mock import patch

from generators.generator_types import Generator
from generators.py_generate import (
    PyGenerator,
    fix_markdown,
    fix_turbo_response,
    handle_first_line_indent,
    handle_entire_body_indent,
    py_fix_indentation,
    py_is_syntax_valid,
    remove_unindented_signatures,
)
from generators.py_generate import (
    PY_SELF_REFLECTION_CHAT_INSTRUCTION,
    PY_SELF_REFLECTION_COMPLETION_INSTRUCTION,
    PY_SELF_REFLECTION_FEW_SHOT,
)


class TestPyGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = PyGenerator()

    def test_self_reflection(self):
        with patch(
            "generators.py_generate.generic_generate_self_reflection"
        ) as mock_reflection:
            # Happy path
            func = "def add(a: int, b: int) -> int: return a - b"
            feedback = "The function should add the numbers, not subtract."
            model = "gpt-3"
            mock_reflection.return_value = "Mocked Reflection"
            result = self.generator.self_reflection(func, feedback, model)
            self.assertEqual(result, "Mocked Reflection")
            mock_reflection.assert_called()

            # Edge case: Empty feedback
            feedback = ""
            mock_reflection.return_value = "Mocked Reflection"
            result = self.generator.self_reflection(func, feedback, model)
            self.assertEqual(result, "Mocked Reflection")

    def test_func_impl(self):
        with patch(
            "generators.py_generate.generic_generate_func_impl"
        ) as mock_func_impl:
            # Happy path
            func_sig = "def add(a: int, b: int) -> int:"
            model = "gpt-3"
            strategy = "simple"
            mock_func_impl.return_value = "Mocked Function Implementation"
            result = self.generator.func_impl(func_sig, model, strategy)
            self.assertEqual(result, "Mocked Function Implementation")
            mock_func_impl.assert_called_once()

    def test_internal_tests(self):
        with patch(
            "generators.py_generate.generic_generate_internal_tests"
        ) as mock_internal_tests:
            # Happy path
            func_sig = "def add(a: int, b: int) -> int:"
            model = "gpt-3"
            mock_internal_tests.return_value = ["Mocked Test"]
            result = self.generator.internal_tests(func_sig, model)
            self.assertEqual(result, ["Mocked Test"])
            mock_internal_tests.assert_called_once()

    def test_handle_first_line_indent(self):
        # Happy path
        func_body = 'print("Hello, world!")'
        expected_output = '    print("Hello, world!")\n'
        self.assertEqual(handle_first_line_indent(func_body), expected_output)

    def test_handle_entire_body_indent(self):
        # Happy path
        func_body = 'print("Hello, world!")\nprint("Another line!")'
        expected_output = (
            "    " + 'print("Hello, world!")\n' + "    " + 'print("Another line!")'
        )
        self.assertEqual(handle_entire_body_indent(func_body), expected_output)

    def test_fix_turbo_response(self):
        # Happy path
        func_body = '```print("Hello, world!") ```'
        expected_output = "    " + 'print("Hello, world!") '
        actual = fix_turbo_response(func_body)
        self.assertEqual(actual, expected_output)

    def test_fix_markdown(self):
        # Happy path
        func_body = '``` print("Hello, world!") ```'
        expected_output = ' print("Hello, world!") '
        self.assertEqual(fix_markdown(func_body), expected_output)

    def test_remove_unindented_signatures(self):
        # Happy path
        func_body = "def add(a, b):\n    return a + b\ndef sub(a, b):\n    return a - b"
        expected_output = "    " + "return a + b\n    return a - b"
        self.assertEqual(remove_unindented_signatures(func_body), expected_output)

    def test_py_fix_indentation(self):
        # Happy path
        func_body = 'print("Hello, world!")'
        expected_output = '    print("Hello, world!")'
        self.assertEqual(py_fix_indentation(func_body), expected_output)

    def test_py_is_syntax_valid(self):
        # Happy path
        code = 'print("Hello, world!")'
        self.assertTrue(py_is_syntax_valid(code))


if __name__ == "__main__":
    unittest.main()
