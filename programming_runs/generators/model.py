class ModelBase():
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'


class GPT4(ModelBase):
    def __init__(self):
        self.name = "gpt-4"


class GPT35(ModelBase):
    def __init__(self):
        self.name = "gpt-3.5-turbo"
