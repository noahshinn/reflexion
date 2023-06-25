from typing import List, Optional, Union
from abc import abstractmethod, ABC

class Generator:
    @abstractmethod
    def self_reflection(self, func: str, feedback: str, model: str) -> str:
        ...

    @abstractmethod
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
        ...

    @abstractmethod
    def internal_tests(
            self,
            func_sig: str,
            model: str,
            committee_size: int = 1,
            max_num_tests: int = 5
    ) -> List[str]:
        ...



class LLMRequest(ABC):
    @abstractmethod
    def completion(
        model: str,
        prompt: str,
        max_tokens: int = 1024,
        stop_strs: Optional[List[str]] = None,
        temperature: float = 0.0,
        num_comps=1,
        ) -> Union[List[str], str]:
        ...
    
    @abstractmethod
    def chat(
        model: str,
        system_message: str,
        user_message: str,
        max_tokens: int = 1024,
        temperature: float = 0.0,
        num_comps=1,
    ) -> Union[List[str], str]: 
        ...