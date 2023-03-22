python main.py \
  --run_name "test_run" \
  --root_dir "root" \
  --dataset_path ./human-eval/data/HumanEval.jsonl.gz \
  --strategy "simple" \
  --model "gpt-4" \
  --pass_at_k "1" \
  --max_iters "1" \
  --verbose
