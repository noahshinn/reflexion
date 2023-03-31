from typing import NamedTuple, List, Tuple


class ExecuteResult(NamedTuple):
    is_passing: bool
    feedback: str
    state: Tuple[bool]


class Executor:
    def execute(self, func: str, tests: List[str], timeout: int = 5) -> ExecuteResult:
        raise NotImplementedError

    def evaluate(self, name: str, func: str, test: str, timeout: int = 5) -> bool:
        raise NotImplementedError

