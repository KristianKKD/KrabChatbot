from elevenlabs.client import ElevenLabs
from elevenlabs import play
from elevenlabs import stream
import asyncio
import warnings
import wave
from TTSImplementation import TextToSpeechBase
warnings.filterwarnings("ignore", category=FutureWarning)

class ElevenLabsTTS(TextToSpeechBase):
    def __init__(self, api_key="", voice="", model_id=""):
        super().__init__(api_key=api_key, voice=voice, model_id=model_id)

    def setup_engine(self, api_key, voice, model_id=""):
        self.elevenlabs = ElevenLabs(
            api_key=api_key,
        )

        if voice == "":
            self.voice = "JBFqnCBsd6RMkjVDRZzb"
        if model_id == "":
            self.model_id = "eleven_flash_v2_5"

    async def generate_audio(self, audio_file):
        audio_iterator = self.elevenlabs.text_to_speech.convert(
            text=self.text,
            voice_id=self.voice,
            model_id=self.model_id,
            output_format="mp3_44100_128",
        )

        # Combine the audio bytes from the iterator
        audio_data = b"".join(audio_iterator)

        # Save the audio data into a .wav file
        with wave.open(audio_file, "wb") as wav_file:
            wav_file.setnchannels(1)  # Mono audio
            wav_file.setsampwidth(2)  # Sample width in bytes (16-bit audio)
            wav_file.setframerate(44100)  # Sample rate
            wav_file.writeframes(audio_data)

    async def play_audio(self, audio_file):
        audio_stream = self.elevenlabs.text_to_speech.stream(
            text=self.text,
            voice_id=self.voice,
            model_id=self.model_id,
            output_format="mp3_44100_128",
        )

        stream(audio_stream)

    def stop_audio(self):
        print("Stopping TTS message: " + self.text)
        self.stream.stop()
        if self.discord_bot is not None:
            self.discord_bot.stop_tts()
