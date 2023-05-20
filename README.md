# Reflexion: Language Agents with Verbal Reinforcement Learning

This repo holds the code, demos, and logs for the Reflexion paper (v2 not out yet): [Reflexion: Language Agents with Verbal Reinforcement Learning. Noah Shinn, Federico Cassano, Beck Labash, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao. _Preprint_, 2023](https://arxiv.org/abs/2303.11366)

![Reflexion RL diagram](./figures/reflexion_rl.png)

![Reflexion tasks](./figures/reflexion_tasks.png)

We release the LeetcodeHardGym [here](https://github.com/GammaTauAI/leetcode-hard-gym)

### Note
`decision-making`: `./alfworld_runs` and `./webshop_runs`
`programming`: v2 not released yet, to be cleaned soon
`reasoning`: `./hotpotqa_runs`

### To Run: decision-making (AlfWorld)
Clone this repo and move to the AlfWorld directory
```bash
git clone https://github.com/noahshinn024/reflexion && cd ./alfworld_runs
```

Specify the run parameters in `./run_reflexion.sh`.
`num_trials`: number of iterative learning steps
`num_envs`: number of task-environment pairs per trial
`run_name`: the name for this run
`use_memory`: use persisting memory to store self-reflections (turn off to run a baseline run)
`is_resume`: use logging directory to resume a previous run
`resume_dir`: the logging directory from which to resume the previous run
`start_trial_num`: if resume run, then the trial number of which to start

Run the trial
```bash
./run_reflexion.sh
```

The logs will be sent to `./root/<run_name>`.

### To Run: reasoning (HotPotQA)
Clone this repo and move to the AlfWorld directory
```bash
git clone https://github.com/noahshinn024/reflexion && cd ./hotpotqa_runs
```

### Another Note

Due to the nature of these experiments, it may not be feasible for individual developers to rerun the results as GPT-4 has limited access and significant API charges. All runs from the paper and additional results are logged in `./alfworld_runs/root` for decision-making and `./hotpotqa_runs/root` for reasoning. 

### Other Notes

Check out the code for the original draft [here](https://github.com/noahshinn024/reflexion-draft)

Read the original blog [here](https://nanothoughts.substack.com/p/reflecting-on-reflexion)

Check out an interesting type-inference implementation here: [OpenTau](https://github.com/GammaTauAI/opentau)

For all questions, contact [noahshinn024@gmail.com](noahshinn024@gmail.com)

### Cite

```bibtex
@article{shinn2023reflexion,
  title={Reflexion: an autonomous agent with dynamic memory and self-reflection},
  author={Shinn, Noah and Labash, Beck and Gopinath, Ashwin},
  journal={arXiv preprint arXiv:2303.11366},
  year={2023}
}
```
