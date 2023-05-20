from langchain.agents.react.base import DocstoreExplorer
from langchain.llms.base import BaseLLM

def reactLLMMock(prompt: str) -> str:
    last_line = prompt.split('\n')[-1].strip()
    last_action = last_line.split(' ')[0].lower()
    if last_action == 'thought':
        return 'It does not mention the eastern sector. So I need to look up eastern sector.'
    elif last_action == 'action':
        return 'Lookup[eastern sector]'
    else:
        raise Exception('Invalid action type')


def reflectLLMMock(prompt: str) -> str:
    return "Last time i should have answered correctly"

class LLMMock(BaseLLM):
    def __init__(self):
        ...
    
    def __call__(self, prompt: str) -> str:
        if prompt.split('\n')[0].split(' ')[0] == 'Solve':
            return reactLLMMock(prompt)
        
        elif prompt.split('\n')[0].split(' ')[0] == 'You':
            return reflectLLMMock(prompt)
        else:
            raise Exception("Invalid LLM prompt")
    
    def get_num_tokens(self, text: str) -> int:
        return 0
    
class DocStoreExplorerMock(DocstoreExplorer):
    def __init__(self):
        self.summary = "The Colorado orogeny was an episode of mountain building (an orogeny) in Colorado and surrounding areas."
        self.body = "(Result 1 / 1) The eastern sector extends into the High Plains and is called the Central Plains orogeny."
    
    def search(self, search: str, sents: int = 5) -> str:
        return self.summary
    
    def lookup(self, term: str) -> str:
        return self.body