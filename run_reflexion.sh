python main.py \
  --run_name "reflexion_scratch" \
  --root_dir "root" \
  --dataset_path ./human-eval/data/HumanEval.jsonl.gz \
  --strategy "reflexion" \
  --language "py" \
  --model "gpt-4" \
  --pass_at_k "1" \
  --max_iters "10" \
  --verbose
