from typing import NamedTuple

class ExecuteResult(NamedTuple):
    is_passing: bool
    feedback: str
