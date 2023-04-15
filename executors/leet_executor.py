from typing import List

from .executor_types import ExecuteResult, Executor
from .executor_utils import to_jsonl
from datetime import datetime

from .leetcode_env.leetcode_env.utils import SubmissionFormatter
from .leetcode_env.leetcode_env.leetcode_types import ProgrammingLanguage

class LeetExecutor(Executor):
    
    def __init__(self, lang: ProgrammingLanguage, executor: Executor, formatter: SubmissionFormatter):
        from .leetcode_env.leetcode_env.environment import LeetCodeEnv
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
        leetcode_formatted_func = self.formatter.to_leetcode(func)
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
