# Reflexion: Language Agents with Verbal Reinforcement Learning

![Reflexion RL diagram](./figures/reflexion_rl.png)

This repo holds the code, demos, and logs for: [Reflexion: Language Agents with Verbal Reinforcement Learning. Noah Shinn, Federico Cassano, Beck Labash, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao. _Preprint_, 2023](https://arxiv.org/abs/2303.11366)

![Reflexion tasks](./figures/reflexion_tasks.png)

We release the LeetcodeHardGym [here](https://github.com/GammaTauAI/leetcode-hard-gym)

### Another Note

Due to the nature of these experiments, it may not be feasible for individual developers to rerun the results as GPT-4 has limited access and significant API charges. All runs from the paper and additional results are logged in `./programming_runs/root` for programming, `./alfworld_runs/root` for decision-making, and `./hotpotqa_runs/root` for reasoning. Programming runs can be validated with scripts [here](https://github.com/noahshinn024/reflexion/blob/main/programming/validate_py_results.py) and [here](https://github.com/noahshinn024/reflexion/blob/main/programming/validate_rs_results.py) to validate the Python and Rust solutions with the unit tests provided by their respective benchmarks.

### Warning

Please do not run the Reflexion programming agent in an unsecure environment as the generated code is not validated before execution.

### Other Notes

Check out the code for the original draft [here](https://github.com/noahshinn024/reflexion-draft)

Read the original blog [here](https://nanothoughts.substack.com/p/reflecting-on-reflexion)

Check out an interesting type-inference implementation here: [OpenTau](https://github.com/GammaTauAI/opentau)

If you have any questions, contact [noahshinn024@gmail.com](noahshinn024@gmail.com)

### Cite

```bibtex
@article{shinn2023reflexion,
  title={Reflexion: an autonomous agent with dynamic memory and self-reflection},
  author={Shinn, Noah and Labash, Beck and Gopinath, Ashwin},
  journal={arXiv preprint arXiv:2303.11366},
  year={2023}
}
```
