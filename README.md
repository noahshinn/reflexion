# Mastering HumanEval with Reflexion

This is a spin-off project inspired by the paper: [Reflexion: an autonomous agent with dynamic memory and self-reflection. Noah Shinn, Beck Labash, Ashwin Gopinath. _Preprint_, 2023](https://arxiv.org/abs/2303.11366)

Read more about this project in this [post](https://nanothoughts.substack.com/p/reflecting-on-reflexion)

Check out an interesting type-inference implementation here: [OpenTau](https://github.com/GammaTauAI/opentau)

Check out the code for the original paper [here](https://github.com/noahshinn024/reflexion)

Check out a new superhuman programming agent gym [here](https://github.com/GammaTauAI/leetcode-hard-gym)

If you have any questions, please contact [noahshinn024@gmail.com](noahshinn024@gmail.com)

![architecture](./media/architecture.png)

![result](./media/performance.png)

### Note

Due to the nature of these experiments, it may not be feasible for individual developers to rerun the results due to limited access to GPT-4 and significant API charges. Due to recent requests, both trials have been rerun once more and are dumped in `./root` with a script [here](https://github.com/noahshinn024/reflexion-human-eval/blob/main/validate_py_results.py) to validate the solutions with the unit tests provided by [HumanEval](https://github.com/openai/human-eval).

To run the validation on your log files or the provided log files:
```bash
python ./validate_py_results.py <path to jsonlines file>
```

### Warning

Please do not run the Reflexion agent in an unsecure environment as the generated code is not validated before execution.

### Cite

**Note**: This is a spin-off implementation that implements a relaxation on the internal success criteria proposed in the [original paper](https://arxiv.org/abs/2303.11366).

```bibtex
@article{shinn2023reflexion,
  title={Reflexion: an autonomous agent with dynamic memory and self-reflection},
  author={Shinn, Noah and Labash, Beck and Gopinath, Ashwin},
  journal={arXiv preprint arXiv:2303.11366},
  year={2023}
}
```
