import logging
from typing import List, Optional, Union

import requests
from .generator_types import LLMRequest
import re
import json


class LocalRequest(LLMRequest):
    def __init__(self, url: str):
        self.url = url

    def extract_first_python_block(self, text):
        # Regular expression pattern to match Python code blocks
        pattern = re.compile(r"```python\r\n(.*?)```", re.DOTALL)

        # Extract all matches
        matches = pattern.findall(text)

        # Return the first match if we found one, or None otherwise
        return matches[0] if matches else None

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
            "model": model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "stop_strs": stop_strs,
            "temperature": temperature,
            "num_comps": num_comps,
        }

        # Make the request
        response = requests.post(self.url, json=params)

        # Check if request is successful
        if response.status_code == 200:
            # Parse the response JSON
            response_json = response.json()

            # Return the appropriate field from the JSON response
            if num_comps == 1:
                response_text = json.loads(response.text)["response"]
                return_value = self.extract_first_python_block(response_text)
                return return_value

            else:
                return None  # Or handle the case where num_comps != 1 as needed
        else:
            logging.error(
                f"HTTP request failed with status code {response.status_code}. Response: {response.text}"
            )
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
        return self.completion(
            self, model, concatenated_message, max_tokens, temperature, num_comps
        )


'''
'Below is an instruction that describes a task. Write a response that appropriately completes the request. \n\n### Instruction: # Write the body of this function only.\n\ndef minSubArraySum(nums):\n    """\n    Given an array of integers nums, find the minimum sum of any non-empty sub-array\n    of nums.\n    Example\n    minSubArraySum([2, 3, 4, 1, 2, 4]) == 1\n    minSubArraySum([-1, -2, -3]) == -6\n    """\n \n### Response:Here\'s the body of the function:\r\n\r\n```python\r\ndef minSubArraySum(nums):\r\n    """\r\n    Given an array of integers nums, find the minimum sum of any non-empty sub-array\r\n    of nums.\r\n    Example\r\n    minSubArraySum([2, 3, 4, 1, 2, 4]) == 1\r\n    minSubArraySum([-1, -2, -3]) == -6\r\n    """\r\n    # Initialize variables\r\n    min_sum = float(\'inf\')\r\n    current_sum = 0\r\n    \r\n    # Loop through the array\r\n    for num in nums:\r\n        # Add the current number to the current sum\r\n        current_sum += num\r\n        \r\n        # If the current sum is less than the minimum sum, update the minimum sum\r\n        if current_sum < min_sum:\r\n            min_sum = current_sum\r\n        \r\n        # If the current sum is greater than or equal to zero, reset the current sum to zero\r\n        if current_sum >= 0:\r\n            current_sum = 0\r\n    \r\n    return min_sum\r\n```\r\n\r\nThis function uses a sliding window approach to find the minimum sum of any non-empty sub-array of the input array. It initializes two variables: `min_sum` and `current_sum`. `min_sum` is initialized to infinity, and `current_sum` is initialized to zero. The function then loops through the input array, adding each number to `current_sum`. If `current_sum` is less than `min_sum`, `min_sum` is updated to `current_sum`. If `current_sum` is greater than or equal to zero, `current_sum` is reset to zero. Finally, the function returns `min_sum`.'

'''
