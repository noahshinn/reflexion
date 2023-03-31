from .py_executor import PyExecutor
from .rs_executor import RsExecutor
from .executor_types import Executor

def executor_factory(lang: str) -> Executor:
    if lang == "py" or lang == "python":
        return PyExecutor()
    elif lang == "rs" or lang == "rust":
        return RsExecutor()
    else:
        raise ValueError(f"Invalid language for executor: {lang}")
