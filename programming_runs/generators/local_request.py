import logging
from typing import List, Optional, Union

import requests
from .generator_types import LLMRequest


class LocalRequest(LLMRequest):

    def __init__(self, url: str):
        self.url = url

    def completion(
        self,
        model: str,
        prompt: str,
        max_tokens: int = 1024,
        stop_strs: Optional[List[str]] = None,
        temperature: float = 0.0,
        num_comps=1,
        ) -> Union[List[str], str]:

        # Define request parameters
        params = {
            'model': model,
            'prompt': prompt,
            'max_tokens': max_tokens,
            'stop_strs': stop_strs,
            'temperature': temperature,
            'num_comps': num_comps
        }

        # Make the request
        response = requests.get(self.url, params=params)
        
        # Check if request is successful
        if response.status_code == 200:
            # Parse the response JSON
            response_json = response.json()

            # Return the appropriate field from the JSON response
            if num_comps == 1:
                return response_json['your_field_here']  # Replace 'your_field_here' with the actual field name
            else:
                return None  # Or handle the case where num_comps != 1 as needed
        else:
            logging.error(f'HTTP request failed with status code {response.status_code}. Response: {response.text}')
            return None  # Or handle the error case as needed
     

     
    def chat(
        self,
        model: str,
        system_message: str,
        user_message: str,
        max_tokens: int = 1024,
        temperature: float = 0.0,
        num_comps=1,
    ) -> Union[List[str], str]: 
        concatenated_message = f"{system_message} \n{user_message}"
        return self.completion(self,model,concatenated_message,max_tokens,temperature,num_comps)
    