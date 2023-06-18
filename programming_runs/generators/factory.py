from .local_request import LocalRequest
from .openai_request import OpenAIRequest
from .py_generate import PyGenerator
from .rs_generate import RsGenerator
from .generator_types import Generator, LLMRequest
from .api_endpoint import endpoint
def generator_factory(lang: str) -> Generator:
    if lang == "py" or lang == "python":
        return PyGenerator()
    elif lang == "rs" or lang == "rust":
        return RsGenerator()
    else:
        raise ValueError(f"Invalid language for generator: {lang}")


def llm_factory()-> LLMRequest:
    
    if endpoint.get_api_endpoint() == None:
        return OpenAIRequest()
    else:
        return LocalRequest(endpoint.get_api_endpoint())
