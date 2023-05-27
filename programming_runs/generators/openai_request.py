from typing import List, Optional, Union
import openai
from .generator_types import LLMRequest


class OpenAIRequest(LLMRequest):
    
    def __init__(self):
        self.openai_module = openai

    def completion(
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
     
    def chat(
        model: str,
        system_message: str,
        user_message: str,
        max_tokens: int = 1024,
        temperature: float = 0.0,
        num_comps=1,
    ) -> Union[List[str], str]: 
         
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
        n=num_comps,
        )
        if num_comps == 1:
            return response.choices[0].message.content  # type: ignore

        return [choice.message.content for choice in response.choices]  # type: ignore


    