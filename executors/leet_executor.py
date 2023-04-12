from typing import List

from .executor_types import ExecuteResult, Executor


class LeetExecutor(Executor):
    from .leetcode_env.leetcode_env.utils import SubmissionFormatter
    from .leetcode_env.leetcode_env.leetcode_types import ProgrammingLanguage

    def __init__(self, lang: ProgrammingLanguage, executor: Executor, formatter: SubmissionFormatter):
        from .leetcode_env.leetcode_env.environment import LeetCodeEnv
        self.lang = lang
        self.executor = executor
        self.formatter = formatter
        self.env = LeetCodeEnv()

    def execute(self, func: str, tests: List[str], timeout: int = 5) -> ExecuteResult:
        return self.executor.execute(func, tests, timeout)

    def evaluate(self, name: str, func: str, test: str, timeout: int = 5) -> bool:
        from .leetcode_env.leetcode_env.utils import id_from_slug
        from .leetcode_env.leetcode_env.leetcode_types import LeetCodeSubmission
        submission = LeetCodeSubmission(
            code=self.formatter.to_leetcode(func),
            lang=self.lang,
            question_id=id_from_slug(name, self.env.api_instance),
            question_slug=name,
            timeout=timeout
        )

        _, reward, _, _ = self.env.step(submission)

        return reward
