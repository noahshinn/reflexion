import torch
from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSeq2SeqLM

"""
Intuitively, AutoModelForSeq2SeqLM is used for language models with encoder-decoder architecture like T5 and BART,
while AutoModelForCausalLM is used for auto-regressive language models like all the GPT models.


Todo: Future versions should use TensorRT for acceleration also looking at BetterTransformer/optimum but they do not support  T5
https://developer.nvidia.com/blog/optimizing-t5-and-gpt-2-for-real-time-inference-with-tensorrt/

"""

app = FastAPI()

model_name = "Salesforce/codet5p-770m-py"
codet5 = "Salesforce/codet5p-770m-py"
model_hermione = "WizardLM/WizardCoder-15B-V1.0"
model_name = model_hermione
load_in_8bit = False
model = AutoModelForCausalLM.from_pretrained(
    model_name, device_map="auto", load_in_8bit=load_in_8bit
).eval()

tokenizer = AutoTokenizer.from_pretrained(model_name)


@app.post("/generate")
def generate_response(request_data: dict):
    data = request_data
    prompt = data["prompt"]
    expected_model = data["model"]
    top_k = data.get("topk",3)
    max_tokens = data.get("max_tokens", 512)
    # Todo will need to write an implementation of this  since this not currently supported by Transformers
    # may ask in huggingface forums
    # stop_strings = data.get("stop_strs")
    temperature = data.get("temperature", 0.7)
    do_sample= data.get("do_sample",True)
    top_p = data.get("top_p",.95)
    # Todo will need to look to see what the best way to implemnt this similar to openai api
    num_comps = data.get("num_comps", 1)

    wrappedprompt = f"Below is an instruction that describes a task. Write a response that appropriately completes the request. \n\n### Instruction: {prompt} \n### Response:"

    if expected_model != model_name:
        return {"error": f"Invalid model name: {expected_model}. Expected {model_name}."}, 400

    with torch.no_grad():
        input_ids = tokenizer.encode(wrappedprompt, return_tensors="pt").to(model.device)
        output = model.generate(
            input_ids,
            max_length=max_tokens,
            num_return_sequences=num_comps,
            do_sample=do_sample,
            top_k=top_k,
            temperature=temperature,
            top_p=top_p,
        )

        response = tokenizer.decode(output[0], skip_special_tokens=True)

    return {"response": response}
