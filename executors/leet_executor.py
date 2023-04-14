from typing import List

from .executor_types import ExecuteResult, Executor
from .executor_utils import to_jsonl
from .leetcode_env.leetcode_env.utils import SubmissionFormatter

from .leetcode_env.leetcode_env.environment import LeetCodeEnv
from .leetcode_env.leetcode_env.leetcode_types import ProgrammingLanguage, LeetCodeSubmission
from .leetcode_env.leetcode_env.utils import id_from_slug

from datetime import datetime

class LeetExecutor(Executor):
    def __init__(self, lang: ProgrammingLanguage, executor: Executor, formatter: SubmissionFormatter):
        self.lang = lang
        self.executor = executor
        self.formatter = formatter
        self.env = LeetCodeEnv()
        self.name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    def execute(self, func: str, tests: List[str], timeout: int = 5) -> ExecuteResult:
        return self.executor.execute(func, tests, timeout)

    def evaluate(self, name: str, func: str, test: str, timeout: int = 5) -> bool:
        print(f'Timeout is {timeout} seconds')
        leetcode_formatted_func = self.formatter.to_leetcode(func)
        print('----------------- LEETCODE SUBMISSION ------------------')
        print(leetcode_formatted_func)
        print('--------------------------------------------------------')
        submission = LeetCodeSubmission(
            code = self.formatter.to_leetcode(func),
            lang = self.lang,
            question_id = id_from_slug(name, self.env.api_instance),
            question_slug = name,
            timeout = timeout
        )

        status, reward, _, info = self.env.step(submission)

        print('----------------- LEETCODE EVALUATION ------------------')
        print(status)
        print(info)
        print('--------------------------------------------------------')

        to_jsonl({
            'code': leetcode_formatted_func,
            'status': status,
            'reward': reward,
            'info': info
        },
        f'{self.name}.jsonl'
        )



        return reward

