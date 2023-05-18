python main.py \
  --run_name "testacc_humaneval_py3" \
  --root_dir "root" \
  --dataset_path ./benchmarks/humaneval-py.jsonl.gz \
  --strategy "test-acc" \
  --language "py" \
  --model "gpt-4" \
  --pass_at_k "1" \
  --max_iters "1" \
  --verbose
