from twitchio.ext import commands
import os
import asyncio
from AIModel import AIModel
from TTS import TextToSpeech

class KrabBot(commands.Bot):
    tts_enabled = False
    model_enabled = False

    model = None
    tts_inprogress = []

    def __init__(self, tts_enabled = False, model = None, model_enabled = False):
        super().__init__(
            token=os.environ["TWITCH_TOKEN"],
            client_id=os.environ["TWITCH_CLIENT_ID"],
            nick='KrabBot',
            prefix='!',
            initial_channels=['KrabGor']
        )
        
        self.model = model

        self.tts_enabled = tts_enabled
        self.model_enabled = model_enabled

    async def connect(self):
        await super().connect()
        await self.enable_tts(self.tts_enabled)
        await self.enable_model(self.model_enabled)

    async def enable_tts(self, enabled):
        print("TTS enabled: " + str(enabled))
        self.tts_enabled = enabled

    async def enable_model(self, enabled):
        print("Model enabled: " + str(enabled))
        self.model_enabled = enabled

        if enabled:
            if self.model is None:
                self.model = AIModel()
            asyncio.create_task(self.model.load_model())
        elif not enabled:
            self.model = None

    async def event_message(self, message):
        usr = message.author.name
        content = message.content

        incoming_message = usr + " says: " + content
        #print(incoming_message)

        if self.tts_enabled:
            asyncio.create_task(self.speak(incoming_message))

        if self.model_enabled:
            asyncio.create_task(self.handle_model_response(incoming_message))

        if self.model:
            asyncio.create_task(self.model.add_to_context(usr, content))

    async def handle_model_response(self, incoming_message):
        response = await self.model.generate_response(incoming_message, False)
        if self.tts_enabled:
            asyncio.create_task(self.speak(response))
        else:
            print("Bot response: " + response)

        if self.model:
            asyncio.create_task(self.model.add_to_context("Me", response))

    async def stop_tts(self):
        print("Stopping all TTS messages")
        for tts in self.tts_inprogress:
            tts.stop()
        self.tts_inprogress = []

    async def clear_model_context(self):
        await self.model.clear_context()

    async def speak(self, text):
        tts = TextToSpeech()
        self.tts_inprogress.append(tts)

        # Run speak in background so it doesn't block
        async def speak_and_cleanup():
            await tts.speak(text)
            if tts in self.tts_inprogress:
                self.tts_inprogress.remove(tts)

        asyncio.create_task(speak_and_cleanup())

