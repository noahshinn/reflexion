from typing import Optional


class APIEndPoint:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.api_endpoint:Optional[str] = None

    def set_api_endpoint(self, value:str):
        self.api_endpoint = value

    def get_api_endpoint(self):
        return self.api_endpoint

endpoint = APIEndPoint()

