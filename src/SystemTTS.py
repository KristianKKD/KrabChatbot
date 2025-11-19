from RealtimeTTS import TextToAudioStream, SystemEngine
import asyncio
import warnings
from TTSImplementation import TextToSpeechBase
warnings.filterwarnings("ignore", category=FutureWarning)

class SystemTTS(TextToSpeechBase):
    def __init__(self, api_key="", voice=""):
        super().__init__(api_key=api_key, voice=voice)

    def setup_engine(self, api_key, voice, model_id=""):
        self.engine = SystemEngine()
        self.stream = TextToAudioStream(self.engine)

    async def generate_audio(self, audio_file):
        self.stream.feed(self.text)
        await asyncio.to_thread(self.stream.play, output_wavfile=audio_file, muted=True)

    async def play_audio(self, audio_file):
        self.stream.feed(self.text)
        await asyncio.to_thread(self.stream.play)

    def stop_audio(self):
        print("Stopping TTS message: " + self.text)
        self.stream.stop()
        if self.discord_bot is not None:
            self.discord_bot.stop_tts()
