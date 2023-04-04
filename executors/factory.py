from .py_executor import PyExecutor, PyLeetExecutor
from .rs_executor import RsExecutor, RsLeetExecutor
from .executor_types import Executor


def executor_factory(lang: str, is_leet: bool = False) -> Executor:
    if lang == "py" or lang == "python":
        if is_leet:
            return PyLeetExecutor()
        else:
            return PyExecutor()
    elif lang == "rs" or lang == "rust":
        if is_leet:
            return RsLeetExecutor()
        else:
            return RsExecutor()
    else:
        raise ValueError(f"Invalid language for executor: {lang}")
