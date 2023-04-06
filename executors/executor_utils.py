def timeout_handler(_, __):
    raise TimeoutError()

import re
from abc import ABC, abstractmethod

class SubmissionFormatter(ABC):
    """
    Class that converts between HumanEval and Leetcode submission formats.
    """
    @abstractmethod
    def to_leetcode(self, humaneval_snippet: str):
        ...
    
    @abstractmethod
    def to_humaneval(self, leetcode_snippet: str):
        ...

class PySubmissionFormatter(SubmissionFormatter):
    def to_leetcode(self, humaneval_snippet: str):
        return f"""\
        class Solution:
            {humaneval_snippet.strip()}
        """
    
    def to_humaneval(self, leetcode_snippet: str):
        pattern = re.compile(r"class Solution:\s+([\s\S]+)")
        match = pattern.search(leetcode_snippet)
        if match:
            return match.group(1).strip()
        return leetcode_snippet.strip()

class RsSubmissionFormatter(SubmissionFormatter):
    def to_leetcode(self, humaneval_snippet: str):
        return f"""\
        impl Solution {{
            {humaneval_snippet.strip()}
        }}
        """

    def to_humaneval(self, leetcode_snippet: str):
        pattern = re.compile(r"impl Solution \{([\s\S]+)\}")
        match = pattern.search(leetcode_snippet)
        if match:
            return match.group(1).strip()
        return leetcode_snippet.strip()

# Py tests

if __name__ == "__main__":
    formatter = PySubmissionFormatter()
    leetcode_1 = 'class Solution:\n    def solveSudoku(self, board: List[List[str]]) -> None:\n        """\n        Do not return anything, modify board in-place instead.\n        """\n        '
    humaneval_1 = 'def solveSudoku(self, board: List[List[str]]) -> None:\n        """\n        Do not return anything, modify board in-place instead.\n        """\n'

    assert leetcode_1 == formatter.to_leetcode(humaneval_1)
    assert humaneval_1 == formatter.to_humaneval(leetcode_1)




