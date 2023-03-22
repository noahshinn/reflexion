from utils import gpt_chat, gpt_completion

from typing import List

FEW_SHOT = """For example:

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

COMPLETION_INSTRUCTION = f"""You are CodexGPT, an AI coding assistant that can write unique, diverse, and intuitive unit tests for functions given the signature and docstring.

{FEW_SHOT}"""

CHAT_INSTRUCTION = """You are CodexGPT, an AI coding assistant that can write unique, diverse, and intuitive unit tests for functions given the signature and docstring."""

def dump_tests(tests: List[str]) -> str:
    """
    Dumps the tests to a string.
    """
    return "\n".join(tests)

def parse_tests(tests: str) -> List[str]:
    """
    Parses the tests from a string.
    """
    return [test.strip() for test in tests.splitlines() if "assert" in test]

# TODO: type-check generated unit tests?
def generate_internal_unit_tests(model: str, func_signature: str, committee_size: int=1) -> List[str]:
    """
    Generates tests for a function using a refinement technique with the number
    of specified commmittee members.
    """
    if model == "gpt-4" or model == "gpt-3.5-turbo":
        message = f'{FEW_SHOT}\n\nfunc signature:\n{func_signature}\nunit tests:'
        output = gpt_chat(model, CHAT_INSTRUCTION, message)
    else:
        prompt = f'{COMPLETION_INSTRUCTION}\n\nfunc signature:\n{func_signature}\nunit tests:'
        output = gpt_completion(model, prompt)
    cur_tests: List[str] = parse_tests(output) # type: ignore

    # TODO: NOT SUPPORTED YET
    # cur_refinement_num = 0
    # while cur_refinement_num < committee_size:
        # # TODO: implement
        # cur_tests = ... # type: ignore

        # cur_refinement_num += 1

    return cur_tests

if __name__ == "__main__":
    s = """def separate_paren_groups(paren_string: str) -> List[str]:
    \"\"\" Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
    separate those group into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    \"\"\""""
    print(generate_internal_unit_tests("gpt-4", s))
