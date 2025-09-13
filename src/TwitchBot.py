from twitchio.ext import commands
import os
import asyncio
from TextToSpeech import TextToSpeech
import Communicate
import keyboard

class KrabBot(commands.Bot):
    tts_enabled = False
    model_enabled = False
    twitch_input_enabled = False

    tts_inprogress = []
    model_busy = False

    def __init__(self, tts_enabled = False, model_enabled = False, twitch_input_enabled = False):
        super().__init__(
            token=os.environ["TWITCH_TOKEN"],
            client_id=os.environ["TWITCH_CLIENT_ID"],
            nick='KrabBot',
            prefix='!',
            initial_channels=['KrabGor']
        )
        
        #enable the settings
        self.tts_enabled = tts_enabled
        self.model_enabled = model_enabled
        self.twitch_input_enabled = twitch_input_enabled

    async def connect(self):
        await super().connect()
        await self.enable_tts(self.tts_enabled)
        await self.enable_model(self.model_enabled)

    async def enable_tts(self, enabled):
        print("TTS enabled: " + str(enabled))
        self.tts_enabled = enabled

    async def enable_model(self, enabled):
        print("Model currently broken...")
        self.model_enabled = False
        return

        print("Model enabled: " + str(enabled))
        self.model_enabled = enabled

    async def enable_twitch_input(self, enabled):
        print("Twitch input enabled: " + str(enabled))
        self.twitch_input_enabled = enabled

    async def event_message(self, message):
        usr = message.author.name
        content = message.content

        if len(content) <= 1 or content[0] != '!':
            return #ignore commands too small
        content = content[1:] #strip the !

        print("-------------incoming_message: User: " + usr + "Message: " + content)

        if self.twitch_input_enabled:
            asyncio.create_task(self.process_twitch_input(content))
        elif not self.model_busy: #don't tts if the model is yapping
            if self.tts_enabled and not self.model_enabled:
                asyncio.create_task(self.speak(content, prefix=usr + " messaged: ", useasync=True, is_ai=False))
            elif self.model_enabled:
                asyncio.create_task(self.handle_model_response(usr, content))
            
        #add to context
        Communicate.add_to_context(usr, content)

    async def handle_model_response(self, usr, content):
        self.model_busy = True #don't respond until done

        #generate a response
        response = await asyncio.to_thread(Communicate.generate_response, f"{usr} said: {content}")

        #speak
        await self.speak(content, prefix=usr + " messaged: ", useasync=False, is_ai=False)

        #read response message out
        if self.tts_enabled:
            await self.speak(response, prefix="Bot response: ", useasync=False, is_ai=True)
        else:
            print("Bot response: " + response)

        #add to context
        Communicate.add_to_context("Me", response)

        self.model_busy = False

    async def stop_tts(self):
        print("Stopping all TTS messages")
        for tts in self.tts_inprogress:
            tts.stop()
        self.tts_inprogress = []
        self.model_busy = False

    async def clear_model_context(self):
        Communicate.clear_context()

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

    async def process_twitch_input(self, content):
        #print("Processing twitch input: " + content)

        translated_inputs = {
                            "forward": "w",
                            "back": "s",
                            "left": "a",
                            "right": "d",
                            "jump": "space",
                            "attack": "lmb"
                            }

        if content not in translated_inputs:
            return

        #press and release the key
        keyboard.press_and_release(translated_inputs[content])