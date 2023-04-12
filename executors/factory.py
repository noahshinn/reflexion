from .leetcode_env.leetcode_env.leetcode_types import ProgrammingLanguage

from .py_executor import PyExecutor
from .rs_executor import RsExecutor
from .leet_executor import LeetExecutor
from .executor_types import Executor
from .leetcode_env.leetcode_env.utils import PySubmissionFormatter, RsSubmissionFormatter

def executor_factory(lang: str, is_leet: bool = False) -> Executor:
    if lang == "py" or lang == "python":
        if is_leet:
            return LeetExecutor(ProgrammingLanguage.PYTHON3,
                                PyExecutor(),
                                PySubmissionFormatter())
        else:
            return PyExecutor()
    elif lang == "rs" or lang == "rust":
        if is_leet:
            return LeetExecutor(ProgrammingLanguage.RUST,
                                RsExecutor(),
                                RsSubmissionFormatter())
        else:
            return RsExecutor()
    else:
        raise ValueError(f"Invalid language for executor: {lang}")
