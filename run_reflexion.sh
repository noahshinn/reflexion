python main.py \
  --run_name "reflexion_human_eval_py_logging" \
  --root_dir "root" \
  --dataset_path ./benchmarks/humaneval-py.jsonl.gz \
  --strategy "reflexion" \
  --language "py" \
  --model "gpt-4" \
  --pass_at_k "1" \
  --max_iters "5" \
  --verbose
