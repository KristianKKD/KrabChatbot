import logging
logging.getLogger("transformers.generation.utils").setLevel(logging.ERROR)

import torch
import transformers
from transformers import pipeline
import gc

class AIModel:
    pipe = None #communicate to model via this
    model_id = "meta-llama/Llama-3.2-1B"

    model_response_prefix = (
        "A viewer says:"
    )
    model_response_suffix = (
        "Here is your reply:"
    )

    max_context_messages = 20
    context = []

    def __init__(self):
        self.pipe = None
        self.context = []

    def __del__(self):
        self.pipe = None
        try:
            torch.cuda.empty_cache()
        except Exception:
            pass
        gc.collect()

    async def load_model(self):
        print("Creating model pipe...")

        self.pipe = pipeline(
            "text-generation",
            model=self.model_id,
            torch_dtype=torch.bfloat16,
            device_map="cuda"
        )

        print("Loading " + self.model_id + "...")

        model = transformers.AutoModelForCausalLM.from_pretrained(
            self.model_id, torch_dtype="auto", cache_dir="E:/AI/models/", device_map="cuda"
        )
        tokenizer = transformers.AutoTokenizer.from_pretrained(
            self.model_id, cache_dir="E:/AI/models/"
        )

        print(self.model_id + " loaded!")

    async def generate_response(self, prompt, temperature=0.7, max_new_tokens=50, raw=False):
        if not self.pipe:
            raise RuntimeError("Model pipeline not initialized.")

        #input and generate output
        context = "".join(self.context[-self.max_context_messages:])
        full_prompt = f"{context} {self.model_response_prefix} \n {prompt}.\n {self.model_response_suffix}"
        if raw:
            full_prompt = prompt

        print(full_prompt)
        output = self.pipe(full_prompt, temperature=temperature, max_new_tokens=max_new_tokens)

        #remove the prompt from the output
        response = output[0]['generated_text']
        response = response.replace(full_prompt, "").strip()
        response = response.replace('\n', '')

        return response

    async def add_to_context(self, user, content):
        entry = user + ":" + content + "\n"
        self.context.append(entry)
        if len(self.context) > self.max_context_messages:
            self.context.pop(0) #remove oldest

    async def clear_context(self):
        self.context = []