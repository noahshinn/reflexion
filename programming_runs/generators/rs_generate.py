from .generator_types import Generator
from .generator_utils import gpt_chat, gpt_completion, generic_generate_func_impl, generic_generate_internal_tests, generic_generate_self_reflection

from typing import List, Optional, Union

RS_SIMPLE_COMPLETION_INSTRUCTION = "// Write the body of this function only."
RS_REFLEXION_COMPLETION_INSTRUCTION = "You are RustGPT. You will be given your past function implementation, a series of unit tests, and a hint to change the implementation appropriately. Apply the changes below by writing the body of this function only.\n\n-----"
RS_SELF_REFLECTION_COMPLETION_INSTRUCTION = "You are RustGPT. You will be given a function implementation and a series of unit tests. Your goal is to write a few sentences to explain why your implementation is wrong as indicated by the tests. You will need this as a hint when you try again later. Only provide the few sentence description in your answer, not the implementation.\n\n-----"

RS_SIMPLE_CHAT_INSTRUCTION = "You are RustGPT. You will be given a function signature and docstring. You should fill in the following text of the missing function body. For example, the first line of the completion should have 4 spaces for the indendation so that it fits syntactically with the preceding signature."
RS_REFLEXION_CHAT_INSTRUCTION = "You are RustGPT. You will be given your past function implementation, a series of unit tests, and a hint to change the implementation appropriately. Apply the changes below by writing the body of this function only. You should fill in the following text of the missing function body. For example, the first line of the completion should have 4 spaces for the indendation so that it fits syntactically with the preceding signature."
RS_SELF_REFLECTION_CHAT_INSTRUCTION = "You are RustGPT. You will be given a function implementation and a series of unit tests. Your goal is to write a few sentences to explain why your implementation is wrong as indicated by the tests. You will need this as a hint when you try again later. Only provide the few sentence description in your answer, not the implementation."

RS_REFLEXION_COMPLETION_INSTRUCTION = "You are a Rust programming assistant. You will be given your past function implementation, a series of unit tests, and a hint to change the implementation appropriately. Apply the changes below by writing the body of this function only.\n\n-----"
RS_SELF_REFLECTION_COMPLETION_INSTRUCTION = "You are a Rust programming assistant. You will be given a function implementation and a series of unit tests. Your goal is to write a few sentences to explain why your implementation is wrong as indicated by the tests. You will need this as a hint when you try again later. Only provide the few sentence description in your answer, not the implementation.\n\n-----"

RS_SIMPLE_CHAT_INSTRUCTION = "You are a Rust programming assistant. You will be given a function signature and docstring. You should fill in the following text of the missing function body. For example, the first line of the completion should have 4 spaces for the indendation so that it fits syntactically with the preceding signature."
RS_REFLEXION_CHAT_INSTRUCTION = "You are a Rust programming assistant. You will be given your past function implementation, a series of unit tests, and a hint to change the implementation appropriately. Apply the changes below by writing the body of this function only. You should fill in the following text of the missing function body. For example, the first line of the completion should have 4 spaces for the indendation so that it fits syntactically with the preceding signature."
RS_SELF_REFLECTION_CHAT_INSTRUCTION = "You are a Rust programming assistant. You will be given a function implementation and a series of unit tests. Your goal is to write a few sentences to explain why your implementation is wrong as indicated by the tests. You will need this as a hint when you try again later. Only provide the few sentence description in your answer, not the implementation."


RS_REFLEXION_FEW_SHOT_ADD = '''Example 1:
[previous impl]:
fn add(a: i32, b: i32) -> i32 {
    // Given integers a and b, return the total value of a and b.
    a - b
}

[unit test results from previous impl]:
Tested passed:

Tests failed:
assert_eq!(add(1, 2), 3); // output: -1
assert_eq!(add(1, 2), 4); // output: -1

[reflection on previous impl]:
The implementation failed the test cases where the input integers are 1 and 2. The issue arises because the code does not add the two integers together, but instead subtracts the second integer from the first. To fix this issue, we should change the operator from `-` to `+` in the return statement. This will ensure that the function returns the correct output for the given input.

[improved impl]:
fn add(a: i32, b: i32) -> i32 {
    // Given integers a and b, return the total value of a and b.
    a + b
}

END EXAMPLES
'''


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

RS_SELF_REFLECTION_FEW_SHOT = '''Example 1:
[function impl]:
pub fn group_anagrams(strs: Vec<String>) -> Vec<Vec<String>> {
// Given an array of strings strs, group the anagrams together. You can return the answer in any order.
// An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.
  use std::collections::HashMap;
  let mut map: HashMap<[u8;26], Vec<String>> = HashMap::with_capacity(strs.len());
  let offset = 'a' as usize;

  for str in strs.into_iter() {
    let mut chars: [u8; 26] = [0; 26];

    for char in str.chars() {
      chars[char.to_ascii_lowercase() as usize - offset] += 1;
    }

    // Flaw: using str.len() instead of chars in the hashmap key
    map.entry(str.len())
      .and_modify(|v| v.push(str.clone()))
      .or_insert(vec![str]);
  }
  
  let mut arr: Vec<Vec<String>> = Vec::new();
  for v in map.into_values() {
    arr.push(v);
  }
  arr
}

[unit test results]:
Tested passed:
assert_eq!(func(vec![""]), vec![vec![""]]);
assert_eq!(func(vec!["a"]), vec![vec!["a"]]);

Tests failed:
assert_eq!(func(vec!["eat", "tea", "tan", "ate", "nat", "bat"]), vec![vec!["bat"], vec!["nat", "tan"], vec!["ate", "eat", "tea"]]); # output:  [["bat", "tan", "nat"], ["eat", "tea", "ate"]]

[self-reflection]:
The implementation failed to group the anagrams together correctly. Instead, it grouped words by their length, which is not the intended behavior. The issue lies in using the length of the input strings (str.len()) as the key for the hashmap, rather than the count of each character in the strings (chars). To overcome this error, I should change the hashmap key to the character count array (chars). This will ensure that words with the same character counts (anagrams) are grouped together, which is the desired output. Next time I approach the problem, I will make sure to use the correct hashmap key to group the anagrams.

END EXAMPLES

'''
RS_TEST_GENERATION_COMPLETION_INSTRUCTION = f"""You are RustGPT, an AI coding assistant that can write unique, diverse, and intuitive unit tests for functions given the signature and docstring.

{RS_TEST_GENERATION_FEW_SHOT}"""

RS_TEST_GENERATION_CHAT_INSTRUCTION = """You are a Rust programming assistant, an AI coding assistant that can write unique, diverse, and intuitive unit tests for functions given the signature and docstring."""


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


class RsGenerator(Generator):
    def self_reflection(self, func: str, feedback: str, model: str) -> str:
        return generic_generate_self_reflection(
            func=func,
            feedback=feedback,
            model=model,
            SELF_REFLECTION_CHAT_INSTRUCTION=RS_SELF_REFLECTION_CHAT_INSTRUCTION,
            SELF_REFLECTION_COMPLETION_INSTRUCTION=RS_SELF_REFLECTION_COMPLETION_INSTRUCTION,
            SELF_REFLECTION_FEW_SHOT=RS_SELF_REFLECTION_FEW_SHOT,
        )

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
            REFLEXION_FEW_SHOT=RS_REFLEXION_FEW_SHOT_ADD,
            fix_body=(lambda x: x)
        )

    def internal_tests(
            self,
            func_sig: str,
            model: str,
            committee_size: int = 1,
            max_num_tests: int = 5
    ) -> List[str]:
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
            is_syntax_valid=(lambda x: True)  # TODO: for now. typecheck maybe?
        )


if __name__ == "__main__":
    # for testing
    pass
