import pytest
from unittest.mock import patch
from .generator_types import Generator
from .py_generator import PyGenerator

class TestPyGenerator:
    @pytest.fixture
    def generator(self):
        return PyGenerator()

    def test_self_reflection(self, generator):
        with patch('py_generator.generic_generate_self_reflection') as mock_reflection:
            # Happy path
            func = "def add(a: int, b: int) -> int: return a - b"
            feedback = "The function should add the numbers, not subtract."
            model = "gpt-3"
            mock_reflection.return_value = 'Mocked Reflection'
            result = generator.self_reflection(func, feedback, model)
            assert result == 'Mocked Reflection'
            mock_reflection.assert_called_once_with(func, feedback, model, generator.SELF_REFLECTION_CHAT_INSTRUCTION, generator.SELF_REFLECTION_COMPLETION_INSTRUCTION, generator.SELF_REFLECTION_FEW_SHOT)

            # Edge case: Empty feedback
            feedback = ""
            mock_reflection.return_value = 'Mocked Reflection'
            result = generator.self_reflection(func, feedback, model)
            assert result == 'Mocked Reflection'

    def test_func_impl(self, generator):
        with patch('py_generator.generic_generate_func_impl') as mock_func_impl:
            # Happy path
            func_sig = "def add(a: int, b: int) -> int:"
            model = "gpt-3"
            strategy = "simple"
            mock_func_impl.return_value = 'Mocked Function Implementation'
            result = generator.func_impl(func_sig, model, strategy)
            assert result == 'Mocked Function Implementation'
            mock_func_impl.assert_called_once()

            # Edge case: Invalid strategy
            with pytest.raises(ValueError):
                generator.func_impl(func_sig, model, 'invalid_strategy')

    def test_internal_tests(self, generator):
        with patch('py_generator.generic_generate_internal_tests') as mock_internal_tests:
            # Happy path
            func_sig = "def add(a: int, b: int) -> int:"
            model = "gpt-3"
            mock_internal_tests.return_value = ['Mocked Test']
            result = generator.internal_tests(func_sig, model)
            assert result == ['Mocked Test']
            mock_internal_tests.assert_called_once()

            # Edge case: Committee size zero
            with pytest.raises(ValueError):
                generator.internal_tests(func_sig, model, committee_size=0)

            # Edge case: Negative max_num_tests
            with pytest.raises(ValueError):
                generator.internal_tests(func_sig, model, max_num_tests=-1)
    

    def test_handle_first_line_indent(self, generator):
        # Happy path
        func_body = 'print("Hello, world!")'
        expected_output = '    print("Hello, world!")'
        assert generator.handle_first_line_indent(func_body) == expected_output

        # Edge case: Already indented
        func_body = '    print("Hello, world!")'
        assert generator.handle_first_line_indent(func_body) == func_body

    def test_handle_entire_body_indent(self, generator):
        # Happy path
        func_body = 'print("Hello, world!")\nprint("Another line!")'
        expected_output = '    print("Hello, world!")\n    print("Another line!")'
        assert generator.handle_entire_body_indent(func_body) == expected_output

        # Edge case: Already indented
        func_body = '    print("Hello, world!")\n    print("Another line!")'
        assert generator.handle_entire_body_indent(func_body) == func_body

    def test_fix_turbo_response(self, generator):
        # Happy path
        func_body = '`{3} print("Hello, world!") `{3}'
        expected_output = ' print("Hello, world!") '
        assert generator.fix_turbo_response(func_body) == expected_output

        # Edge case: No markdown backticks
        func_body = 'print("Hello, world!")'
        assert generator.fix_turbo_response(func_body) == func_body

    def test_fix_markdown(self, generator):
        # Happy path
        func_body = '`{3} print("Hello, world!") `{3}'
        expected_output = ' print("Hello, world!") '
        assert generator.fix_markdown(func_body) == expected_output

        # Edge case: No markdown backticks
        func_body = 'print("Hello, world!")'
        assert generator.fix_markdown(func_body) == func_body

    def test_remove_unindented_signatures(self, generator):
        # Happy path
        func_body = 'def add(a, b):\n    return a + b\ndef sub(a, b):\n    return a - b'
        expected_output = '    def add(a, b):\n    return a + b\ndef sub(a, b):\n    return a - b'
        assert generator.remove_unindented_signatures(func_body) == expected_output

        # Edge case: All indented
        func_body = '    def add(a, b):\n    return a + b\n    def sub(a, b):\n    return a - b'
        assert generator.remove_unindented_signatures(func_body) == func_body

    def test_py_fix_indentation(self, generator):
        # Happy path
        func_body = 'print("Hello, world!")'
        expected_output = '    print("Hello, world!")'
        assert generator.py_fix_indentation(func_body) == expected_output

        # Edge case: Already indented
        func_body = '    print("Hello, world!")'
        assert generator.py_fix_indentation(func_body) == func_body

    def test_py_is_syntax_valid(self, generator):
        # Happy path
        code = 'print("Hello, world!")'
        assert generator.py_is_syntax_valid(code) == True

        # Edge case: Invalid syntax
        code = 'print("Hello, world'
        assert generator.py_is_syntax_valid(code) == False
