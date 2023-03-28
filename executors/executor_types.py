from typing import NamedTuple, List, Tuple


class ExecuteResult(NamedTuple):
    is_passing: bool
    feedback: str
    state: Tuple[bool]
