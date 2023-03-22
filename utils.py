import os
import gzip
import json
import openai
import jsonlines
from tenacity import (
    retry,
    stop_after_attempt, # type: ignore
    wait_random_exponential, # type: ignore
)

from typing import Union, List, Optional

openai.api_key = os.getenv("OPENAI_API_KEY")

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def gpt_completion(
        model: str,
        prompt: Union[str, List[str]],
        max_tokens: int = 256,
        stop_strs: Optional[List[str]] = None,
        temperature: float = 0.0,
    ) -> Union[str, List[str]]:
    # check if batched or not
    is_batched = isinstance(prompt, list)
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=stop_strs,
    )
    if is_batched:
        res: List[str] = [""] * len(prompt)
        for choice in response.choices: # type: ignore
            res[choice.index] = choice.text
        return res
    return response.choices[0].text # type: ignore

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def gpt_chat(
        model: str,
        system_message: str,
        user_message: str,
        max_tokens: int = 256,
        temperature: float = 0.0,
    ) -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    return response.choices[0].message.content # type: ignore

def read_jsonl(path: str) -> List[dict]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File `{path}` does not exist.")
    elif not path.endswith(".jsonl"):
        raise ValueError(f"File `{path}` is not a jsonl file.")
    items = []
    with jsonlines.open(path) as reader:
        for item in reader:
            items += [item]
    return items

def write_jsonl(path: str, data: List[dict], append: bool = False):
    if not path.endswith(".jsonl"):
        raise ValueError(f"File `{path}` is not a jsonl file.")
    with jsonlines.open(path, mode='a' if append else 'w') as writer:
        for item in data:
            writer.write(item)

def read_jsonl_gz(path: str) -> List[dict]:
    if not path.endswith(".jsonl.gz"):
        raise ValueError(f"File `{path}` is not a jsonl.gz file.")
    with gzip.open(path, "rt") as f:
        data = [json.loads(line) for line in f]
    return data

def parse_body(text):
    lines = text.split('\n')
    for i in range(len(lines)-1, -1, -1):
        if 'return' in lines[i]:
            return '\n'.join(lines[:i+1])
    return text

def build_asserts_from_human_eval(text: str, func_name: str) -> List[str]:
    asserts = []
    for line in text.splitlines():
        if "assert" in line:
            asserts += [line.strip().replace("candidate", func_name)]
    return asserts
