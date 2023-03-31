from typing import List, Optional, Union


class Generator:
    def self_reflection(self, func: str, feedback: str, model: str) -> str:
        raise NotImplementedError

    def func_impl(
        self,
        func_sig: str,
        model: str,
        strategy: str,
        prev_func_impl: Optional[str] = None,
        feedback: Optional[str] = None,
        self_reflection: Optional[str] = None,
        num_comps: int = 1,
        temperature: float = 0.0,
    ) -> Union[str, List[str]]:
        raise NotImplementedError

    def internal_tests(
            self,
            func_sig: str,
            model: str,
            committee_size: int = 1,
            max_num_tests: int = 5
    ) -> List[str]:
        raise NotImplementedError
