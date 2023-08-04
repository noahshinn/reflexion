from typing import List, Union, Optional, Literal
import dataclasses

from tenacity import (
    retry,
    stop_after_attempt,  # type: ignore
    wait_random_exponential,  # type: ignore
)
import openai

MessageRole = Literal["system", "user", "assistant"]
@dataclasses.dataclass()
class Message():
    role: MessageRole
    content: str


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def gpt_completion(
        model: str,
        prompt: str,
        max_tokens: int = 1024,
        stop_strs: Optional[List[str]] = None,
        temperature: float = 0.0,
        num_comps=1,
) -> Union[List[str], str]:
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=stop_strs,
        n=num_comps,
    )
    if num_comps == 1:
        return response.choices[0].text  # type: ignore

    return [choice.text for choice in response.choices]  # type: ignore


@retry(wait=wait_random_exponential(min=1, max=180), stop=stop_after_attempt(6))
def gpt_chat(
    model: str,
    messages: List[Message],
    max_tokens: int = 1024,
    temperature: float = 0.0,
    num_comps=1,
) -> Union[List[str], str]:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[dataclasses.asdict(message) for message in messages],
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        n=num_comps,
    )
    if num_comps == 1:
        return response.choices[0].message.content  # type: ignore

    return [choice.message.content for choice in response.choices]  # type: ignore

class ModelBase():
    def __init__(self, name: str):
        self.name = name
        self.is_chat = False

    def __repr__(self) -> str:
        return f'{self.name}'

    def generate_chat(self, messages: List[Message], max_tokens: int = 1024, temperature: float = 0.2, num_comps: int = 1) -> Union[List[str], str]:
        raise NotImplementedError

    def generate(self, prompt: str, max_tokens: int = 1024, stop_strs: Optional[List[str]] = None, temperature: float = 0.0, num_comps=1) -> Union[List[str], str]:
        raise NotImplementedError


class GPTChat(ModelBase):
    def __init__(self, model_name: str):
        self.name = model_name
        self.is_chat = True

    def generate_chat(self, messages: List[Message], max_tokens: int = 1024, temperature: float = 0.2, num_comps: int = 1) -> Union[List[str], str]:
        return gpt_chat(self.name, messages, max_tokens, temperature, num_comps)


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
        import torch
        from transformers import pipeline
        self.name = "star-chat"
        self.pipe = pipeline(
            "text-generation", model="HuggingFaceH4/starchat-beta", torch_dtype=torch.bfloat16, device_map="auto")
        self.is_chat = True

    def generate_chat(self, messages: List[Message], max_tokens: int = 1024, temperature: float = 0.2, num_comps: int = 1) -> Union[List[str], str]:
        # NOTE: HF does not like temp of 0.0. 
        if temperature < 0.0001:
            temperature = 0.0001
        
        prompt = ""
        for i, message in enumerate(messages):
            prompt += f"<|{message.role}|>\n{message.content}<|end|>\n"
            if i == len(messages) - 1:
                prompt += "\n<|assistant|>"
        
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
