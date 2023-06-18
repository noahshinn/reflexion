from transformers import AutoModelForCausalLM, AutoTokenizer

codet5 = "Salesforce/codet5p-770m-py"
model_hermione = "WizardLM/WizardCoder-15B-V1.0"
model_name = model_hermione
model = AutoModelForCausalLM.from_pretrained(
    model_name, device_map="auto", load_in_8bit=True
).eval()
prompt = "write a python function to add two numbers return only the method and no other text Response:"
tokenizer = AutoTokenizer.from_pretrained(model_name)
input_ids = tokenizer.encode(prompt, return_tensors="pt").to(model.device)
max_tokens = 400
temperature = 0.7
output = model.generate(
    input_ids,
    max_length=max_tokens,
    # num_return_sequences=1,
    # do_sample=True,
    # top_k=3,
    #   temperature=temperature,
    #   top_p=0.95,
)

response = tokenizer.decode(output[0], skip_special_tokens=True)
print(response)
