import os
from typing import List
import dotenv

import gym
import tiktoken
from langchain import OpenAI
from langchain.llms.base import BaseLLM
from langchain.prompts import PromptTemplate

from environment import QAEnv
from prompts import reflect_prompt, react_agent_prompt, react_reflect_agent_prompt, REFLECTION_HEADER
from fewshots import WEBTHINK_SIMPLE6, REFLECTIONS

dotenv.load_dotenv()

class ReactAgent:
    """
    A question answering ReAct Agent.
    """
    def __init__(self,
                 question: str,
                 env: QAEnv,
                 agent_prompt: PromptTemplate = react_agent_prompt,
                 react_llm: BaseLLM = OpenAI(
                                             temperature=0,
                                             max_tokens=100,
                                             model_name="text-davinci-003",
                                             model_kwargs={"stop": "\n"},
                                             openai_api_key=os.environ['OPENAI_API_KEY']),
                 ) -> None:
        
        self.question = question
        self.agent_prompt = agent_prompt
        self.react_examples = WEBTHINK_SIMPLE6

        self.env = env
        self.env.reset()
        self.reset()
        self.truncated, self.reward, self.terminated = False, False, False

        self.llm = react_llm
        
        self.enc = tiktoken.encoding_for_model("text-davinci-003")

    def run(self, reset = True) -> None:
        if reset:
            self.env.reset()
            self.reset()
        
        while not (self.is_truncated() or self.is_terminated()):
            self.step()
    
    def step(self) -> None:
        # Think
        self.scratchpad += f'\nThought {self.curr_step}:'
        self.scratchpad += ' ' + self.prompt_agent()
        print(self.scratchpad.split('\n')[-1])

        # Act
        self.scratchpad += f'\nAction {self.curr_step}:'
        action = self.prompt_agent()
        self.scratchpad += ' ' + action
        print(self.scratchpad.split('\n')[-1])

        # Observe
        self.scratchpad += f'\nObservation {self.curr_step}: '
        observation, self.reward, self.terminated, self.truncated, self.curr_step = self.env.step(action)
        self.scratchpad += observation
        print(self.scratchpad.split('\n')[-1])

    def prompt_agent(self) -> str:
        return format_step(self.llm(self._build_agent_prompt()))
    
    def _build_agent_prompt(self) -> str:
        return self.agent_prompt.format(
                            examples = self.react_examples,
                            question = self.question,
                            scratchpad = self.scratchpad)
    
    def is_terminated(self) -> bool:
        return self.env.is_terminated()

    def is_correct(self) -> bool:
        return self.env.is_correct()

    def is_truncated(self) -> bool:
        return self.env.is_truncated() or (len(self.enc.encode(self._build_agent_prompt())) > 3896)

    def reset(self) -> None:
        self.scratchpad = ''
        self.curr_step = 1


class ReactReflectAgent(ReactAgent):
    """
    A question answering Self-Reflecting React Agent.
    """
    def __init__(self,
                 question: str,
                 env: QAEnv,
                 agent_prompt: PromptTemplate = react_reflect_agent_prompt,
                 reflect_prompt: PromptTemplate = reflect_prompt,
                 react_llm: BaseLLM = OpenAI(
                                             temperature=0,
                                             max_tokens=100,
                                             model_name="text-davinci-003",
                                             model_kwargs={"stop": "\n"},
                                             openai_api_key=os.environ['OPENAI_API_KEY']),
                 reflect_llm: BaseLLM = OpenAI(
                                               temperature=0,
                                               max_tokens=250,
                                               model_name="text-davinci-003",
                                               openai_api_key=os.environ['OPENAI_API_KEY']),
                 ) -> None:
        
        super().__init__(question, env, agent_prompt, react_llm)
        self.reflect_llm = reflect_llm
        self.reflect_prompt = reflect_prompt
        self.reflect_examples = REFLECTIONS
        self.reflections = []
    
    def run(self, reset = True) -> None:
        if (self.is_terminated() or self.is_truncated()) and not self.is_correct():
            self.reflect()

        ReactAgent.run(self, reset)
    
    def reflect(self) -> None:
        self.reflections.append(self.prompt_reflection())
    
    def prompt_reflection(self) -> str:
        return format_step(self.reflect_llm(self._build_reflection_prompt()))


    def _build_reflection_prompt(self) -> str:
        return self.reflect_prompt.format(
                            examples = self.reflect_examples,
                            question = self.question,
                            scratchpad = self._format_scratchpad())
    
    def _build_agent_prompt(self) -> str:
        return self.agent_prompt.format(
                            examples = self.react_examples,
                            reflections = format_reflections(self.reflections),
                            question = self.question,
                            scratchpad = self.scratchpad)
    
    def _format_scratchpad(self) -> str:
        lines = self.scratchpad.split('\n')
        lines_by_tokens = sorted(lines, key=lambda x: len(self.enc.encode(x)))
        while len(self.enc.encode('\n'.join(lines))) > 1600:
            ind = lines.index(lines_by_tokens.pop(-1))
            line = lines[ind]
            lines[ind]  = line.split(':')[0] + ': ...'
        return '\n'.join(lines)
    
    

### String Operations ###
def format_reflections(reflections: List[str]) -> str:
    if reflections == []:
        return ''
    else:
        header = REFLECTION_HEADER
        return header + 'Reflections:\n- ' + '\n- '.join([r.strip() for r in reflections])

def format_step(step: str) -> str:
    return step.strip('\n').strip().replace('\n', '')



