import os
import asyncio
import warnings
from Integration_Discord import DiscordBot
from abc import ABC, abstractmethod

warnings.filterwarnings("ignore", category=FutureWarning)

_tts_id_counter:int = 0

class TextToSpeechBase(ABC):
    text:str = ""
    id:int = 0
    voice:str = ""
    model_id:str = ""
    discord_bot:DiscordBot = None

    def __init__(self, api_key:str="", voice:str="", model_id:str=""):
        print("Creating TTS instance")

        self.voice = voice
        self.model_id = model_id
        self.discord_bot = None

        global _tts_id_counter
        self.id = _tts_id_counter
        _tts_id_counter += 1

        self.setup_engine(api_key, voice)
        return

    def __del__(self):
        #print("Deleting TTS instance")
        return
        
    async def speak(self, text, discord_bot, user = "", obs_comms = None):
        self.text = text
        print(f"{user} said:{text}")

        if obs_comms is not None:
            obs_comms.set_text(text, user)

        audio_filename:str = "output" + str(self.id) + ".wav"
        audio_path:str = os.path.join(os.getcwd(), 'audio', audio_filename)

        if discord_bot is not None:
            await self.generate_audio(audio_path)
            await discord_bot.queue_play(audio_path)
        else:
            await self.play_audio(audio_path)

        if obs_comms is not None:
            obs_comms.hide_text()

    def stop_audio(self):
        print("Stopping TTS message: " + self.text)
        self.stream.stop()
        if self.discord_bot is not None:
            self.discord_bot.stop_tts()
        return
    
    @abstractmethod
    async def setup_engine(self, api_key:str, voice:str, model_id:str=""):
        """Initialize the TTS engine. Must be implemented by subclasses."""
        pass

    @abstractmethod
    async def generate_audio(self, audio_path:str):
        """Generate audio file from text. Must be implemented by subclasses."""
    
    @abstractmethod
    async def play_audio(self, audio_path:str):
        """Play the generated audio. Must be implemented by subclasses."""
        pass
