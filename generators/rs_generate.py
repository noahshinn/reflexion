from .generator_utils import gpt_chat, gpt_completion, generic_generate_func_impl, generic_generate_internal_tests, generic_generate_self_reflection

from typing import List, Optional, Union

RS_SIMPLE_COMPLETION_INSTRUCTION = "// Write the body of this function only."
RS_REFLEXION_COMPLETION_INSTRUCTION = "You are RustGPT. You will be given your past function implementation, a series of unit tests, and a hint to change the implementation appropriately. Apply the changes below by writing the body of this function only.\n\n-----"
RS_SELF_REFLECTION_COMPLETION_INSTRUCTION = "You are RustGPT. You will be given a function implementation and a series of unit tests. Your goal is to write a few sentences to explain why your implementation is wrong as indicated by the tests. You will need this as a hint when you try again later. Only provide the few sentence description in your answer, not the implementation.\n\n-----"
RS_SIMPLE_CHAT_INSTRUCTION = "You are RustGPT. You will be given a function signature and docstring. You should fill in the following text of the missing function body. For example, the first line of the completion should have 4 spaces for the indendation so that it fits syntactically with the preceding signature."
RS_REFLEXION_CHAT_INSTRUCTION = "You are RustGPT. You will be given your past function implementation, a series of unit tests, and a hint to change the implementation appropriately. Apply the changes below by writing the body of this function only. You should fill in the following text of the missing function body. For example, the first line of the completion should have 4 spaces for the indendation so that it fits syntactically with the preceding signature."
RS_SELF_REFLECTION_CHAT_INSTRUCTION = "You are RustGPT. You will be given a function implementation and a series of unit tests. Your goal is to write a few sentences to explain why your implementation is wrong as indicated by the tests. You will need this as a hint when you try again later. Only provide the few sentence description in your answer, not the implementation."


RS_TEST_GENERATION_FEW_SHOT = """For example:

func signature:
/// For a given number n, find the largest number that divides n evenly, smaller than n
/// >>> largest_divisor(15)
/// 5
fn largest_divisor(n: isize) -> isize {
    for i in (1..n).rev() {
        if n % i == 0 {
            return i;
        }
    }
    // if no divisor is found, return 1
    1
}

unit tests:
assert_eq!(candidate(3), 1);
assert_eq!(candidate(7), 1);
assert_eq!(candidate(10), 5);
assert_eq!(candidate(100), 50);
assert_eq!(candidate(49), 7);
"""

RS_TEST_GENERATION_COMPLETION_INSTRUCTION = f"""You are RustGPT, an AI coding assistant that can write unique, diverse, and intuitive unit tests for functions given the signature and docstring.

{RS_TEST_GENERATION_FEW_SHOT}"""

RS_TEST_GENERATION_CHAT_INSTRUCTION = """You are RustGPT, an AI coding assistant that can write unique, diverse, and intuitive unit tests for functions given the signature and docstring."""



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


def rs_generate_self_reflection(func: str, feedback: str, model: str) -> str:
    return generic_generate_self_reflection(
        func=func,
        feedback=feedback,
        model=model,
        SELF_REFLECTION_CHAT_INSTRUCTION=RS_SELF_REFLECTION_CHAT_INSTRUCTION,
        SELF_REFLECTION_COMPLETION_INSTRUCTION=RS_SELF_REFLECTION_COMPLETION_INSTRUCTION,
    )


def rs_generate_func_impl(
    func_sig: str,
    model: str,
    strategy: str,
    prev_func_impl: Optional[str] = None,
    feedback: Optional[str] = None,
    self_reflection: Optional[str] = None,
    num_comps: int = 1,
    temperature: float = 0.0,
) -> Union[str, List[str]]:
    return generic_generate_func_impl(
        func_sig=func_sig,
        model=model,
        strategy=strategy,
        prev_func_impl=prev_func_impl,
        feedback=feedback,
        self_reflection=self_reflection,
        num_comps=num_comps,
        temperature=temperature,
        REFLEXION_CHAT_INSTRUCTION=RS_REFLEXION_CHAT_INSTRUCTION,
        SIMPLE_CHAT_INSTRUCTION=RS_SIMPLE_CHAT_INSTRUCTION,
        REFLEXION_COMPLETION_INSTRUCTION=RS_REFLEXION_COMPLETION_INSTRUCTION,
        SIMPLE_COMPLETION_INSTRUCTION=RS_SIMPLE_COMPLETION_INSTRUCTION,
        fix_body=(lambda x: x)
    )


def rs_generate_internal_tests(func_sig: str, model: str, committee_size: int = 1, max_num_tests: int = 5) -> List[str]:
    def parse_tests(tests: str) -> List[str]:
        return [test + ";" for test in tests.split(";")]
    """
    Generates tests for a function using a refinement technique with the number
    of specified commmittee members.
    """
    return generic_generate_internal_tests(
        func_sig=func_sig,
        model=model,
        committee_size=committee_size,
        max_num_tests=max_num_tests,
        TEST_GENERATION_FEW_SHOT=RS_TEST_GENERATION_FEW_SHOT,
        TEST_GENERATION_CHAT_INSTRUCTION=RS_TEST_GENERATION_CHAT_INSTRUCTION,
        TEST_GENERATION_COMPLETION_INSTRUCTION=RS_TEST_GENERATION_COMPLETION_INSTRUCTION,
        parse_tests=parse_tests,
        is_syntax_valid=(lambda x: True) # TODO: for now. typecheck maybe?
    )


if __name__ == "__main__":
    # for testing
    pass
