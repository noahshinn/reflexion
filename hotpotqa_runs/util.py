import os
import json
import joblib
from typing import Dict

def summarize_trial(agents):
    correct = [a for a in agents if a.is_correct()]
    incorrect = [a for a in agents if a.is_finished() and not a.is_correct()]
    return correct, incorrect

def remove_fewshot(prompt: str) -> str:
    prefix = prompt.split('Here are some examples:')[0]
    suffix = prompt.split('(END OF EXAMPLES)')[1]
    return prefix.strip('\n').strip() + '\n' +  suffix.strip('\n').strip()

def log_trial(agents, trial_n):
    correct, incorrect = summarize_trial(agents)

    log = f"""
########################################
BEGIN TRIAL {trial_n}
Trial summary: Correct: {len(correct)}, Incorrect: {len(incorrect)}
#######################################
"""

    log += '------------- BEGIN CORRECT AGENTS -------------\n\n'
    for agent in correct:
        log += remove_fewshot(agent._build_agent_prompt()) + f'\nCorrect answer: {agent.key}\n\n'

    log += '------------- BEGIN INCORRECT AGENTS -----------\n\n'
    for agent in incorrect:
        log += remove_fewshot(agent._build_agent_prompt()) + f'\nCorrect answer: {agent.key}\n\n'

    return log

def summarize_react_trial(agents):
    correct = [a for a in agents if a.is_correct()]
    halted = [a for a in agents if a.is_halted()]
    incorrect = [a for a in agents if a.is_finished() and not a.is_correct()]
    return correct, incorrect, halted

def log_react_trial(agents, trial_n):
    correct, incorrect, halted = summarize_react_trial(agents)

    log = f"""
########################################
BEGIN TRIAL {trial_n}
Trial summary: Correct: {len(correct)}, Incorrect: {len(incorrect)}, Halted: {len(halted)}
#######################################
"""

    log += '------------- BEGIN CORRECT AGENTS -------------\n\n'
    for agent in correct:
        log += remove_fewshot(agent._build_agent_prompt()) + f'\nCorrect answer: {agent.key}\n\n'

    log += '------------- BEGIN INCORRECT AGENTS -----------\n\n'
    for agent in incorrect:
        log += remove_fewshot(agent._build_agent_prompt()) + f'\nCorrect answer: {agent.key}\n\n'

    log += '------------- BEGIN HALTED AGENTS -----------\n\n'
    for agent in halted:
        log += remove_fewshot(agent._build_agent_prompt()) + f'\nCorrect answer: {agent.key}\n\n'

    return log

def save_agents(agents, dir: str):
    os.makedirs(dir, exist_ok=True)
    for i, agent in enumerate(agents):
        print(f'Saving agent {i}...')
        joblib.dump(agent, os.path.join(dir, f'{i}.joblib'))

def save_results(agents, results: Dict, run_dir: str):
    result_file = os.path.join(run_dir, f'{len(agents)}_questions_results.json')
    # Check if result file exists
    existing_results = []
    if os.path.exists(result_file):
        # Load existing results
        with open(result_file, 'r') as f:
            existing_results = json.load(f)
    # Add new results
    existing_results.extend(results)
    with open(os.path.join(run_dir, f'{len(agents)}_questions_results.json'), 'w') as f:
        json.dump(existing_results, f)