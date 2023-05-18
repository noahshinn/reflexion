from .generator_types import Generator
from .generator_utils import generic_generate_func_impl, generic_generate_internal_tests, generic_generate_self_reflection

from typing import Optional, List, Union
import ast
import re

PY_SIMPLE_COMPLETION_INSTRUCTION = "# Write the body of this function only."
PY_REFLEXION_COMPLETION_INSTRUCTION = "You are a Python writing assistant. You will be given your past function implementation, a series of unit tests, and a hint to change the implementation appropriately. Apply the changes below by writing the body of this function only.\n\n-----"
PY_SELF_REFLECTION_COMPLETION_INSTRUCTION = "You are a Python writing assistant. You will be given a function implementation and a series of unit tests. Your goal is to write a few sentences to explain why your implementation is wrong as indicated by the tests. You will need this as a hint when you try again later. Only provide the few sentence description in your answer, not the implementation.\n\n-----"

PY_SIMPLE_CHAT_INSTRUCTION = "You are a Python writing assistant, an AI that only responds with python code, NOT ENGLISH. You will be given a function signature and its docstring by the user. Respond only in code with correct implementation of the function. Do not include provided the docstring in your response."
PY_REFLEXION_CHAT_INSTRUCTION = "You are a Python writing assistant. You will be given your past function implementation, a series of unit tests, and a hint to change the implementation appropriately. Apply the changes below by writing the body of this function only. You should fill in the following text of the missing function body. For example, the first line of the completion should have 4 spaces for the indendation so that it fits syntactically with the preceding signature."
PY_SELF_REFLECTION_CHAT_INSTRUCTION = "You are a Python writing assistant. You will be given a function implementation and a series of unit tests. Your goal is to write a few sentences to explain why your implementation is wrong as indicated by the tests. You will need this as a hint when you try again later. Only provide the few sentence description in your answer, not the implementation."

PY_TEST_GENERATION_FEW_SHOT = """For example:

func signature:
def has_close_elements(numbers: List[float], threshold: float) -> bool:
    \"\"\" Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    \"\"\"

unit tests:
assert has_close_elements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3) == True
assert has_close_elements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05) == False
assert has_close_elements([1.0, 2.0, 5.9, 4.0, 5.0], 0.95) == True
assert has_close_elements([1.0, 2.0, 5.9, 4.0, 5.0], 0.8) == False
assert has_close_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.0], 0.1) == True
assert has_close_elements([1.1, 2.2, 3.1, 4.1, 5.1], 1.0) == True
assert has_close_elements([1.1, 2.2, 3.1, 4.1, 5.1], 0.5) == False"""

PY_TEST_GENERATION_COMPLETION_INSTRUCTION = f"""You are a Python writing assistant, an AI coding assistant that can write unique, diverse, and intuitive unit tests for functions given the signature and docstring.

{PY_TEST_GENERATION_FEW_SHOT}"""

PY_TEST_GENERATION_CHAT_INSTRUCTION = """You are a Python writing assistant, an AI coding assistant that can write unique, diverse, and intuitive unit tests for functions given the signature and docstring."""

class PyGenerator(Generator):
    def self_reflection(self, func: str, feedback: str, model: str) -> str:
        x = generic_generate_self_reflection(
            func=func,
            feedback=feedback,
            model=model,
            SELF_REFLECTION_CHAT_INSTRUCTION=PY_SELF_REFLECTION_CHAT_INSTRUCTION,
            SELF_REFLECTION_COMPLETION_INSTRUCTION=PY_SELF_REFLECTION_COMPLETION_INSTRUCTION,
        )
        return x

    def func_impl(
        self,
        func_sig: str,
        model: str,
        strategy: str,
        prev_func_impl: Optional[str] = None,
        feedback: Optional[str] = None,
        self_reflection: Optional[str] = None,
        num_comps: int = 1,
        temperature: float = 0.0,
    ) -> Union[str, List[str]]:
        x = generic_generate_func_impl(
            func_sig=func_sig,
            model=model,
            strategy=strategy,
            prev_func_impl=prev_func_impl,
            feedback=feedback,
            self_reflection=self_reflection,
            num_comps=num_comps,
            temperature=temperature,
            REFLEXION_CHAT_INSTRUCTION=PY_REFLEXION_CHAT_INSTRUCTION,
            SIMPLE_CHAT_INSTRUCTION=PY_SIMPLE_CHAT_INSTRUCTION,
            REFLEXION_COMPLETION_INSTRUCTION=PY_REFLEXION_COMPLETION_INSTRUCTION,
            SIMPLE_COMPLETION_INSTRUCTION=PY_SIMPLE_COMPLETION_INSTRUCTION,
            fix_body=fix_turbo_response if strategy == "simple" else py_fix_indentation
        )
        return x


    def internal_tests(self, func_sig: str, model: str, committee_size: int = 1, max_num_tests: int = 5) -> List[str]:
        def parse_tests(tests: str) -> List[str]:
            return [test.strip() for test in tests.splitlines() if "assert" in test]
        """
        Generates tests for a function using a refinement technique with the number
        of specified commmittee members.
        """
        x = generic_generate_internal_tests(
            func_sig=func_sig,
            model=model,
            committee_size=committee_size,
            max_num_tests=max_num_tests,
            TEST_GENERATION_FEW_SHOT=PY_TEST_GENERATION_FEW_SHOT,
            TEST_GENERATION_CHAT_INSTRUCTION=PY_TEST_GENERATION_CHAT_INSTRUCTION,
            TEST_GENERATION_COMPLETION_INSTRUCTION=PY_TEST_GENERATION_COMPLETION_INSTRUCTION,
            parse_tests=parse_tests,
            is_syntax_valid=py_is_syntax_valid,
        )
        return x


DUMMY_FUNC_SIG = "def func():"
DUMMY_FUNC_CALL = "func()"


def handle_first_line_indent(func_body: str) -> str:
    if func_body.startswith("    "):
        return func_body
    split = func_body.splitlines()
    return f"    {split[0]}\n" + "\n".join(split[1:])


def handle_entire_body_indent(func_body: str) -> str:
    split = func_body.splitlines()
    res = "\n".join(["    " + line for line in split])
    return res

def fix_turbo_response(func_body: str) -> str:
    return fix_markdown(remove_unindented_signatures(func_body))

def fix_markdown(func_body: str) -> str:
    return re.sub("`{3}", "", func_body)

def remove_unindented_signatures(code: str) -> str:
    regex = r"^def\s+\w+\s*\("

    before_signature = []
    after_signature = []
    signature_found = False

    for line in code.split("\n"):
        if re.match(regex, line):
            signature_found = True
            continue
        
        if signature_found:
            after_signature.append(line)
        else:
            if not line.startswith("    ") and line.strip():
                line = "    " + line
            before_signature.append(line)

    return "\n".join(before_signature + after_signature)


def py_fix_indentation(func_body: str) -> str:
    func_body = fix_turbo_response(func_body)
    """
    3 cases:
        1. good syntax
        2. first line not good
        3. entire body not good
    """
    def parse_indent_rec(f_body: str, cur_state: int) -> str:
        f_body = fix_markdown(f_body)
        if cur_state > 1:
            return f_body
        code = f'{DUMMY_FUNC_SIG}\n{f_body}\n{DUMMY_FUNC_CALL}'
        try:
            exec(code)
            return f_body
        except (IndentationError, SyntaxError):
            p_func = handle_first_line_indent if cur_state == 0 else handle_entire_body_indent
            return parse_indent_rec(p_func(func_body), cur_state + 1)
        except Exception:
            return f_body
    return parse_indent_rec(func_body, 0)


def py_is_syntax_valid(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except Exception:
        return False
