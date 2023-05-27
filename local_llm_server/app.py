import torch
from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer,AutoModelForSeq2SeqLM
'''
Intuitively, AutoModelForSeq2SeqLM is used for language models with encoder-decoder architecture like T5 and BART,
while AutoModelForCausalLM is used for auto-regressive language models like all the GPT models.


Todo: Future versions should use TensorRT for acceleration also looking at BetterTransformer/optimum but they do not support  T5
https://developer.nvidia.com/blog/optimizing-t5-and-gpt-2-for-real-time-inference-with-tensorrt/

'''

app = FastAPI()

model_name  = "Salesforce/codet5p-770m-py"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, device_map="auto").eval()

tokenizer = AutoTokenizer.from_pretrained(model_name)

@app.post("/generate")
def generate_response(request_data: dict):
    data = request_data.get_json()
    prompt = data["prompt"]
    model = data["model"]
    max_tokens = data.get("max_tokens", 1024)
    #Todo will need to write an implementation of this  since this not currently supported by Transformers
    # may ask in huggingface forums
    stop_strings = data.get("stop_strs")
    temperature = data.get("temperature", 0.0)
    #Todo will need to look to see what the best way to implemnt this similar to openai api
    num_comps = data.get("num_comps", 1)

    if model != model_name:
        return {"error": f"Invalid model name: {model}. Expected {model_name}."}, 400
    
    with torch.no_grad():
        input_ids = tokenizer.encode(prompt, return_tensors="pt")
        output = model.generate(
        input_ids,
        max_length=max_tokens,
        num_return_sequences=1,
        do_sample=True,
        temperature=temperature,
        early_stopping=True,
        )

        response = tokenizer.decode(output[0], skip_special_tokens=True)
        
    return {"response": response}