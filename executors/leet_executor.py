from __future__ import annotations

from typing import List

from .executor_types import ExecuteResult, Executor
from .executor_utils import to_jsonl
from datetime import datetime

class LeetExecutor(Executor):
    def __init__(self, lang, executor: Executor, formatter):
        from .leetcode_env.leetcode_env.utils import SubmissionFormatter
        from .leetcode_env.leetcode_env.leetcode_types import ProgrammingLanguage
        from .leetcode_env.leetcode_env.environment import LeetCodeEnv
        assert isinstance(formatter, SubmissionFormatter)
        assert isinstance(lang, ProgrammingLanguage)
        self.lang = lang
        self.executor = executor
        self.formatter = formatter
        self.env = LeetCodeEnv()
        self.name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    def execute(self, func: str, tests: List[str], timeout: int = 5) -> ExecuteResult:
        return self.executor.execute(func, tests, timeout)

    def evaluate(self, name: str, func: str, test: str, timeout: int = 5) -> bool:
        from .leetcode_env.leetcode_env.leetcode_types import LeetCodeSubmission
        from .leetcode_env.leetcode_env.utils import id_from_slug
        print(f'Timeout is {timeout} seconds')
        try:
            leetcode_formatted_func = self.formatter.to_leetcode(func)
        except Exception as e:
            print(f'Error formatting function to leetcode: {e}')
            return False
        print('----------------- LEETCODE SUBMISSION ------------------')
        print(leetcode_formatted_func)
        print('--------------------------------------------------------')
        submission = LeetCodeSubmission(
            code=leetcode_formatted_func,
            lang=self.lang,
            question_id=id_from_slug(name, self.env.api_instance),
            question_slug=name,
            timeout=timeout
        )

        status, reward, _, info = self.env.step(submission)

        print('----------------- LEETCODE SUBMISSION ------------------')
        print(status)
        print('--------------------------------------------------------')

        to_jsonl({
            'name': name,
            'status': status,
            'reward': reward,
            'info': info
        }, self.name)

        return reward
