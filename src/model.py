import torch
import transformers
from transformers import pipeline
import gc

model = None

class AIModel:
    pipe = None #communicate to model via this
    enabled = False
    model_id = "meta-llama/Llama-3.2-1B"
    model_prefix = (
        "This is a relaxed, friendly, and conversational response for a livestream chat. "
        "The responder is casual, approachable, and engaging, chatting naturally with viewers. "
        "They use everyday language, show personality and humor, and keep things light. "
        "They answer questions directly, as if replying to a friend, and keep the conversation welcoming and on-topic. "
        "No need to be overly formal—just be yourself and respond to what the viewer said. "
        "The responder avoids repetition, adapts their tone to the chat's mood, and treats every viewer with kindness and respect. "
        "They draw from a wide range of knowledge and experience, and always aim to make the chat fun and inclusive. "
        "Most importantly, the response should stay tightly focused on the topic or question the viewer brought up, without going off on tangents or adding unrelated information. "
        "A viewer says:"
    )
    model_suffix = (
        "Now, reply to the viewer in a natural, easygoing way—just like you would in a real conversation. "
        "Keep it friendly, clear, and relaxed, and make sure your answer feels like a direct response, not a continuation or monologue. "
        "Focus your answer entirely on the viewer's topic or question, addressing it directly and thoroughly, without drifting into unrelated subjects or unnecessary elaboration. "
        "Feel free to use humor or casual expressions, and focus on making the viewer feel welcome and heard. "
        "Your response should be concise, positive, and engaging, helping to foster a lively and enjoyable chat atmosphere. "
        "Remember to keep things on-topic and approachable for everyone watching. Here is your reply:"
    )

    def __init__(self, ai_model_enabled=False):
        self.pipe = None
        self.enabled = ai_model_enabled
        return

    def __del__(self):
        self.pipe = None
        try:
            torch.cuda.empty_cache()
        except Exception:
            pass
        gc.collect()

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

    async def generate_response(self, prompt, temperature=0.7, max_new_tokens=200, raw=False):
        if not self.pipe:
            raise RuntimeError("Model pipeline not initialized.")

        #input and generate output
        full_prompt = f"{self.model_prefix}. {prompt} . {self.model_suffix}"
        if raw:
            full_prompt = prompt

        output = self.pipe(full_prompt, temperature=temperature, max_new_tokens=200)

        #remove the prompt from the output
        response = output[0]['generated_text']
        response = response.replace(full_prompt, "").strip()

        return response

