from typing import List

from .executor_types import ExecuteResult, Executor
from .leetcode_env.leetcode_env.utils import SubmissionFormatter

from .leetcode_env.leetcode_env.environment import LeetCodeEnv
from .leetcode_env.leetcode_env.leetcode_types import ProgrammingLanguage, LeetCodeSubmission
from .leetcode_env.leetcode_env.utils import id_from_slug

class LeetExecutor(Executor):
    def __init__(self, lang: ProgrammingLanguage, executor: Executor, formatter: SubmissionFormatter):
        self.lang = lang
        self.executor = executor
        self.formatter = formatter
        self.env = LeetCodeEnv()
    
    def execute(self, func: str, tests: List[str], timeout: int = 5) -> ExecuteResult:
        return self.executor.execute(func, tests, timeout)

    def evaluate(self, name: str, func: str, test: str, timeout: int = 5) -> bool:
        submission = LeetCodeSubmission(
            code = self.formatter.to_leetcode(func),
            lang = self.lang,
            question_id = id_from_slug(name, self.env.api_instance),
            question_slug = name,
            timeout = timeout
        )

        _, reward, _, _ = self.env.step(submission)

        return reward

