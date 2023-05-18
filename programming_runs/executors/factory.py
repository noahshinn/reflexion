from .py_executor import PyExecutor
from .rs_executor import RsExecutor
from .executor_types import Executor
from .leet_executor import LeetExecutor

def executor_factory(lang: str, is_leet: bool = False) -> Executor:
    if lang == "py" or lang == "python":
        if is_leet:
            print("Using LeetCode Python executor")
            from .leetcode_env.leetcode_env.leetcode_types import ProgrammingLanguage
            from .leetcode_env.leetcode_env.utils import PySubmissionFormatter, RsSubmissionFormatter
            return LeetExecutor(ProgrammingLanguage.PYTHON3,
                                PyExecutor(),
                                PySubmissionFormatter)
        else:
            return PyExecutor()
    elif lang == "rs" or lang == "rust":
        if is_leet:
            from .leetcode_env.leetcode_env.leetcode_types import ProgrammingLanguage
            from .leetcode_env.leetcode_env.utils import PySubmissionFormatter, RsSubmissionFormatter
            return LeetExecutor(ProgrammingLanguage.RUST,
                                RsExecutor(),
                                RsSubmissionFormatter)
        else:
            return RsExecutor()
    else:
        raise ValueError(f"Invalid language for executor: {lang}")
