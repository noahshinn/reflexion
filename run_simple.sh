python main.py \
  --run_name "simple_human_eval_py_logging" \
  --root_dir "root" \
  --dataset_path ./benchmarks/humaneval-py.jsonl.gz \
  --strategy "simple" \
  --language "py" \
  --model "gpt-4" \
  --pass_at_k "1" \
  --max_iters "1" \
  --verbose
