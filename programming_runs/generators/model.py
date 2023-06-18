from typing import List, Union, Optional
from generators.generator_utils import gpt_chat, gpt_completion


class ModelBase():
    def __init__(self, name: str):
        self.name = name
        self.is_chat = False

    def __repr__(self) -> str:
        return f'{self.name}'

    def generate_chat(self, system_message: str, user_message: str, max_tokens=1024, temperature=0.2, num_comps=1) -> Union[List[str], str]:
        raise NotImplementedError

    def generate(self, prompt: str, max_tokens: int = 1024, stop_strs: Optional[List[str]] = None, temperature: float = 0.0, num_comps=1) -> Union[List[str], str]:
        raise NotImplementedError


class GPTChat(ModelBase):
    def __init__(self, model_name: str):
        self.name = model_name
        self.is_chat = True

    def generate_chat(self, system_message: str, user_message: str, max_tokens=1024, temperature=0.2, num_comps=1) -> Union[List[str], str]:
        return gpt_chat(self.name, system_message, user_message,
                        max_tokens, temperature, num_comps)


class GPT4(GPTChat):
    def __init__(self):
        super().__init__("gpt-4")


class GPT35(GPTChat):
    def __init__(self):
        super().__init__("gpt-3.5-turbo")


class GPTDavinci(ModelBase):
    def __init__(self, model_name: str):
        self.name = model_name

    def generate(self, prompt: str, max_tokens: int = 1024, stop_strs: Optional[List[str]] = None, temperature: float = 0, num_comps=1) -> Union[List[str], str]:
        return gpt_completion(self.name, prompt, max_tokens, stop_strs, temperature, num_comps)


class StarChat(ModelBase):
    def __init__(self):
        from transformers import pipeline
        self.name = "star-chat"
        self.pipe = pipeline(
            "text-generation", model="HuggingFaceH4/starchat-beta")
        self.template = "<|system|>\n{system}<|end|>\n<|user|>\n{query}<|end|>\n<|assistant|>"
        self.is_chat = True

    def generate_chat(self, system_message: str, user_message: str, max_tokens=1024, temperature=0.2, num_comps=1) -> Union[List[str], str]:
        prompt = self.template.format(
            system=system_message, query=user_message)
        outputs = self.pipe(
            prompt,
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=temperature,
            top_p=0.95,
            eos_token_id=49155,
            num_return_sequences=num_comps,
        )

        outs = [output['generated_text'] for output in outputs]  # type: ignore
        assert isinstance(outs, list)
        for i, out in enumerate(outs):
            assert isinstance(out, str)
            out = out.split("<|assistant|>")[1]
            if out.endswith("<|end|>"):
                out = out[:-len("<|end|>")]

            outs[i] = out

        if len(outs) == 1:
            return outs[0]  # type: ignore
        else:
            return outs  # type: ignore
