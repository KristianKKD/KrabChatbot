import os
import asyncio
import warnings
from DiscordIntegration import DiscordBot
from abc import ABC, abstractmethod

warnings.filterwarnings("ignore", category=FutureWarning)

_tts_id_counter = 0

class TextToSpeechBase(ABC):
    text : str
    id : int

    voice : str
    model_id : str
    
    discord_bot : DiscordBot

    def __init__(self, api_key="", voice="", model_id=""):
        print("Creating TTS instance")

        self.voice = voice
        self.model_id = model_id

        self.discord_bot = None

        global _tts_id_counter
        self.id = _tts_id_counter
        _tts_id_counter += 1

        self.setup_engine(api_key, voice)

    def __del__(self):
        #print("Deleting TTS instance")
        return
        
    async def speak(self, text, discord_bot, user = "", obs_comms = None):
        self.text = text
        print(user + " said:" + text)

        if obs_comms is not None:
            obs_comms.set_text(text, user)

        audio_filename = "output" + str(self.id) + ".wav"
        audio_path = os.path.join(os.getcwd(), 'audio', audio_filename)

        if discord_bot is not None:
            await self.generate_audio(audio_path)
            await discord_bot.queue_play(audio_path)
        else:
            await self.play_audio(audio_path)

        if obs_comms is not None:
            obs_comms.hide_text()

    @abstractmethod
    async def setup_engine(self, api_key, voice, model_id=""):
        """Initialize the TTS engine. Must be implemented by subclasses."""
        pass

    @abstractmethod
    async def generate_audio(self, audio_file):
        """Generate audio file from text. Must be implemented by subclasses."""
    
    @abstractmethod
    async def play_audio(self, audio_file):
        """Play the generated audio. Must be implemented by subclasses."""
        pass

    @abstractmethod
    async def stop_audio(self):
        """Stop the generated audio. Must be implemented by subclasses."""
        pass