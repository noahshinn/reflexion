python main.py \
  --run_name "reflexion_star_chat" \
  --root_dir "root" \
  --dataset_path ./benchmarks/humaneval-py.jsonl \
  --strategy "reflexion" \
  --language "py" \
  --model "starchat" \
  --pass_at_k "1" \
  --max_iters "3" \
  --verbose
