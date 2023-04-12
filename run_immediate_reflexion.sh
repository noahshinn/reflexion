python main.py \
  --run_name "immediate_reflexion_mbpp_py3" \
  --root_dir "root" \
  --dataset_path ./benchmarks/humaneval-py.jsonl.gz \
  --strategy "immediate-reflexion" \
  --language "py" \
  --model "gpt-4" \
  --pass_at_k "1" \
  --max_iters "5" \
  --verbose
