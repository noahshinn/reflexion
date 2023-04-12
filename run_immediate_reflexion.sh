python main.py \
  --run_name "reflexion_mbpp_py3" \
  --root_dir "root" \
  --dataset_path ./benchmarks/mbpp-py.jsonl \
  --strategy "immediate-reflexion" \
  --language "py" \
  --model "gpt-4" \
  --pass_at_k "1" \
  --max_iters "5" \
  --verbose
