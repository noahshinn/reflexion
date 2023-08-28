from .py_generate import PyGenerator
from .rs_generate import RsGenerator
from .generator_types import Generator
from .model import CodeLlama, ModelBase, GPT4, GPT35, StarChat, GPTDavinci


def generator_factory(lang: str) -> Generator:
    if lang == "py" or lang == "python":
        return PyGenerator()
    elif lang == "rs" or lang == "rust":
        return RsGenerator()
    else:
        raise ValueError(f"Invalid language for generator: {lang}")


def model_factory(model_name: str) -> ModelBase:
    if model_name == "gpt-4":
        return GPT4()
    elif model_name == "gpt-3.5-turbo":
        return GPT35()
    elif model_name == "starchat":
        return StarChat()
    elif model_name == "codellama":
        return CodeLlama()
    elif model_name.startswith("text-davinci"):
        return GPTDavinci(model_name)
    else:
        raise ValueError(f"Invalid model name: {model_name}")
