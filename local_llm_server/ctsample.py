import ctranslate2
import transformers

print("Loading model...")
generator = ctranslate2.Generator(
    "/workspace/dockerdrive/projects/ct2models/wizardcoder", device="cuda"
)
print("Model loaded.")
print("Loading tokenizer...")
tokenizer = transformers.AutoTokenizer.from_pretrained("WizardLM/WizardCoder-15B-V1.0")
prompt = "<fim_prefix>def print_hello_world():\n    <fim_suffix>\n    print('Hello world!')<fim_middle>"
wizard_prompt = 'Below is an instruction that describes a task. Write a response that appropriately completes the request. \n\n### Instruction: # Write the body of this function only.\n\ndef minSubArraySum(nums):\n    """\n    Given an array of integers nums, find the minimum sum of any non-empty sub-array\n    of nums.\n    Example\n    minSubArraySum([2, 3, 4, 1, 2, 4]) == 1\n    minSubArraySum([-1, -2, -3]) == -6\n    """\n \n### Response: '
final_prompt = wizard_prompt
tokens = tokenizer.convert_ids_to_tokens(tokenizer.encode(final_prompt))

results = generator.generate_batch(
    [tokens], max_length=512, include_prompt_in_result=True
)

text = tokenizer.decode(results[0].sequences_ids[0])
print(text)
