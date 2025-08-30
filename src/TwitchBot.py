from sympy import content
from twitchio.ext import commands
import os
import asyncio
from AIModel import AIModel
from TextToSpeech import TextToSpeech

class KrabBot(commands.Bot):
    tts_enabled = False
    model_enabled = False

    model = None
    tts_inprogress = []
    model_busy = False

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

        print("-------------incoming_message: User: " + usr + "Message: " + content)

        if not self.model_busy: #don't tts if the model is yapping
            if self.tts_enabled and not self.model_enabled:
                asyncio.create_task(self.speak(content, prefix=usr + " messaged: ", useasync=True, is_ai=False))
            elif self.model_enabled and content[1] == '!':
                asyncio.create_task(self.handle_model_response(usr, content))
            
        if self.model:
            asyncio.create_task(self.model.add_to_context(usr, content))

    async def handle_model_response(self, usr, content):
        self.model_busy = True #don't respond until done

        #generate a response and read it out
        response = asyncio.create_task(self.model.generate_response(usr + " said: " + content))

        #speak user message
        await self.speak(content, prefix=usr + " messaged: ", useasync=False, is_ai=False)

        #read response message out
        response = await response
        if self.tts_enabled:
            await self.speak(response, prefix="Bot response: ", useasync=False, is_ai=True)
        else:
            print("Bot response: " + response)

        #add to context
        if self.model:
            await self.model.add_to_context("Me", response)

    async def stop_tts(self):
        print("Stopping all TTS messages")
        for tts in self.tts_inprogress:
            tts.stop()
        self.tts_inprogress = []
        self.model_busy = False

    async def clear_model_context(self):
        await self.model.clear_context()

    async def speak(self, text = "", prefix = "", useasync = True, is_ai = False):
        tts = TextToSpeech()
        self.tts_inprogress.append(tts)

        #run in background so no blocking
        async def speak_and_cleanup():
            await tts.speak(text, prefix=prefix)
            if tts in self.tts_inprogress:
                self.tts_inprogress.remove(tts)
            if is_ai:
                self.model_busy = False

        if useasync:
            asyncio.create_task(speak_and_cleanup())
        else:
            await speak_and_cleanup()

