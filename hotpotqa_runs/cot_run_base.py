import joblib
from react_cls import CoTAgent
from mocks import DocStoreExplorerMock, LLMMock
import numpy as np

def summarize_trial(agents):
    correct = [a for a in agents if a.is_correct()]
    incorrect = [a for a in agents if a.is_finished() and not a.is_correct()]
    return correct, incorrect

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
        log += f'Context: {agent.context} Question: {agent.question}{agent.scratchpad}\nCorrect answer: {agent.key}\n\n'

    log += '------------- BEGIN INCORRECT AGENTS -----------\n\n'
    for agent in incorrect:
        log += f'Context: {agent.context} Question: {agent.question}{agent.scratchpad}\nCorrect answer: {agent.key}\n\n'
    return log

if __name__ == '__main__':
    hotpot = joblib.load('data/hotpot-qa-distractor-sample.joblib').reset_index(drop = True)
    hotpot['supporting_paragraphs'] = None
    for ind, row in hotpot.iterrows():
        supporting_articles = row['supporting_facts']['title']
        articles = row['context']['title']
        sentences = row['context']['sentences'] 
        supporting_paragraphs = []
        for article in supporting_articles:
            supporting_paragraph = ''.join(sentences[np.where(articles == article)][0])
            supporting_paragraphs.append(supporting_paragraph)
        hotpot.at[ind, 'supporting_paragraphs'] = supporting_paragraphs

    for ind, row in hotpot.iterrows():
        supporting_paragraphs = row['supporting_paragraphs']
        supporting_paragraphs = '\n\n'.join(supporting_paragraphs)
        hotpot.at[ind, 'supporting_paragraphs'] = supporting_paragraphs

    agents = [CoTAgent(row['question'], row['supporting_paragraphs'], row['answer']) for _, row in hotpot.iterrows()]
    trial = 0
    log = ''
    for agent in [a for a in agents if not a.is_correct()]:
        agent.run(reflect = False)
        print(f'Answer: {agent.key}')
    trial += 1

    log += log_trial(agents, trial)
    correct, incorrect = summarize_trial(agents)
    print(f'Finished Trial {trial}, Correct: {len(correct)}, Incorrect: {len(incorrect)}')
    dicts = [dict(a.__dict__) for a in agents]
    for d in dicts:
        for k, v in d.items():
            d[k] = str(v)

    joblib.dump(dicts, 'output/base_cot/cot_reflect_50_correct_dicts-8-trials.joblib')
    print(log)

    with open('output/base_cot/100_questions_8_trials.txt', 'w') as f:
        f.write(log)

    trial = 0
    log = ''
    q = 0
    agents_to_run = [a for a in agents if not a.is_correct()]

    while q < len(agents_to_run):
        print(f'Trial: {trial} ({q}/{len(agents_to_run)})')
        agents_to_run[q].run()
        q += 1

    trial += 1

    log += log_trial(agents, trial)
    correct, incorrect, halted = summarize_trial(agents)
    print(f'Finished Trial {trial}, Correct: {len(correct)}, Incorrect: {len(incorrect)}, Halted: {len(halted)}')
