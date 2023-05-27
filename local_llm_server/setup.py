import os

# Step 1: Create app.py
app_code = """
from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "gpt2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

app = FastAPI()

@app.post("/generate")
def generate_response(prompt: str, max_tokens: int):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output = model.generate(input_ids, max_length=max_tokens, num_return_sequences=1)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return {"response": response}
"""

with open("app.py", "w") as file:
    file.write(app_code)


# Step 2: Create setup.sh
setup_code = """
#!/bin/bash

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
"""

with open("setup.sh", "w") as file:
    file.write(setup_code)


# Step 3: Create start.sh
start_code = """
#!/bin/bash

source env/bin/activate
uvicorn app:app --reload
"""

with open("start.sh", "w") as file:
    file.write(start_code)


# Step 4: Create requirements.txt
requirements = [
    "fastapi",
    "uvicorn",
    "transformers"
]

with open("requirements.txt", "w") as file:
    file.write("\n".join(requirements))


# Step 5: Make the shell scripts executable
os.chmod("setup.sh", 0o755)
os.chmod("start.sh", 0o755)
