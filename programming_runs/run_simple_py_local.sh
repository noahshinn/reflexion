python main.py \
  --run_name "simple_humaneval_py_hardest50" \
  --root_dir "root" \
  --dataset_path ./benchmarks/humaneval-py_hardest50.jsonl \
  --strategy "simple" \
  --language "py" \
  --model "WizardLM/WizardCoder-15B-V1.0" \
  --pass_at_k "1" \
  --max_iters "1" \
  --api_endpoint "http://0.0.0.0:8081/generate" \
  --verbose

