import torch
import transformers
from transformers import pipeline
import gc

model = None

class AIModel:
    pipe = None #communicate to model via this
    enabled = False
    model_id = "meta-llama/Llama-3.2-1B"

    def __init__(self, ai_model_enabled=False):
        self.pipe = None
        self.enabled = ai_model_enabled
        return

    async def create_model(self):
        await self.load_model()

        self.pipe = pipeline(
            "text-generation",
            model=self.model_id,
            torch_dtype=torch.bfloat16,
            device_map="cuda"
        )

        self.enabled = True
        return

    async def disable_model(self):
        self.enabled = False
        self.pipe = None
        torch.cuda.empty_cache()
        gc.collect()
        return

    async def load_model(self):
        print("Loading model...")

        model = transformers.AutoModelForCausalLM.from_pretrained(
            self.model_id, torch_dtype="auto", cache_dir="E:/AI/models/", device_map="cuda"
        )
        tokenizer = transformers.AutoTokenizer.from_pretrained(
            self.model_id, cache_dir="E:/AI/models/"
        )

        print(self.model_id + " loaded.")
        return

    async def generate_response(self, prompt, temperature=0.7, max_new_tokens=500):
        if not self.pipe:
            raise RuntimeError("Model pipeline not initialized.")
        
        output = self.pipe(prompt, temperature=temperature, max_new_tokens=max_new_tokens)
        return output[0]['generated_text']

