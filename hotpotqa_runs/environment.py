import re
import string
from typing import Tuple

import gym
from langchain import Wikipedia
from langchain.agents.react.base import DocstoreExplorer

class QAEnv(gym.Env):
    def __init__(self,
                 question: str,
                 key: str,
                 max_steps: int = 6,
                 explorer: DocstoreExplorer = DocstoreExplorer(Wikipedia())):
        
        self.question = question
        self.key = key
        self.max_steps = max_steps
        self.explorer = explorer

        self.reset()

    def reset(self):
          self.curr_step = 0
          self.terminated = False
          self.answer = ''

    def step(self, action: str) -> Tuple[str, bool, bool, bool, bool]:
        action_type, argument = parse_action(action)

        if action_type == 'Finish':
            self.answer = argument
            if self.is_correct():
                observation = 'Answer is CORRECT'
            else: 
                observation = 'Answer is INCORRECT'
            self.terminated = True

        elif action_type == 'Search':
            try:
                observation = self.explorer.search(argument).strip('\n').strip()
            except Exception as e:
                print(e)
                observation = f'Could not find that page, please try again.'
                    
        elif action_type == 'Lookup':
            try:
                observation = self.explorer.lookup(argument).strip('\n').strip()
            except ValueError:
                observation = f'The last page Searched was not found, so you cannot Lookup a keyword in it. Please try one of the similar pages given.'

        else:
            observation = 'Invalid Action. Valid Actions are Lookup[<topic>] Search[<topic>] and Finish[<answer>].'

        reward = self.is_correct()
        terminated = self.is_terminated()
        truncated = self.is_truncated()

        self.curr_step += 1

        return observation, reward, terminated, truncated, self.curr_step

    def is_correct(self) -> bool:
        return EM(self.answer, self.key)
    
    def is_terminated(self) -> bool:
        return self.terminated

    def is_truncated(self) -> bool:
        return self.curr_step >= self.max_steps

def parse_action(string):
    pattern = r'^(\w+)\[(.+)\]$'
    match = re.match(pattern, string)
    
    if match:
        action_type = match.group(1)
        argument = match.group(2)
        return action_type, argument
    
    else:
        return None, None

def normalize_answer(s):
  def remove_articles(text):
    return re.sub(r"\b(a|an|the)\b", " ", text)
  
  def white_space_fix(text):
      return " ".join(text.split())

  def remove_punc(text):
      exclude = set(string.punctuation)
      return "".join(ch for ch in text if ch not in exclude)

  def lower(text):
      return text.lower()

  return white_space_fix(remove_articles(remove_punc(lower(s))))

def EM(answer, key) -> bool:
    return normalize_answer(answer) == normalize_answer(key)
