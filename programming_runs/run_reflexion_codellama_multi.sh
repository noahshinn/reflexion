CUDA_VISIBLE_DEVICES=$1 python main.py \
  --run_name "reflexion_codellama_$1" \
  --root_dir "root" \
  --dataset_path ./benchmarks/humaneval-py.jsonl \
  --strategy "reflexion" \
  --language "py" \
  --model "codellama" \
  --pass_at_k "1" \
  --max_iters "2" \
  --verbose | tee ./logs/reflexion_codellama_$1
