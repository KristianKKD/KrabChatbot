import os
from RealtimeTTS import TextToAudioStream, AzureEngine
import asyncio
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import random
from functools import partial

class TextToSpeech:
    text : str
    id : int

    def __init__(self, id):
        print("Creating TTS instance")
        self.engine = AzureEngine(speech_key=os.environ["AZURE_SPEECH_KEY"], service_region="uksouth")
        self.stream = TextToAudioStream(self.engine)
        self.stream.engine.set_voice("LolaNeural")
        self.id = id

    def __del__(self):
        #print("Deleting TTS instance")
        self.stream.stop()

    async def speak(self, text, discord_bot = None, prefix = "Speaking text: "):
        print(prefix + text)
        self.text = text
        self.stream.feed(text)

        voices = self.stream.engine.get_voices()
        random_index = random.randint(0, len(voices) - 1)
        #self.stream.engine.set_voice(voices[random_index])

        audio_filename = "output.wav" + str(self.id)
        audio_path = os.path.join(os.path.dirname(__file__), '../web/audio', audio_filename)

        if discord_bot is not None:
            await asyncio.to_thread(self.stream.play, output_wavfile=audio_path, muted=True)
            await discord_bot.queue_play(audio_path)
        else:
            await asyncio.to_thread(self.stream.play)

    def stop(self):
        print("Stopping TTS message: " + self.text)
        self.stream.stop()

    def send_to_web(self, text):
        from web_display import update_web_display

        audio_filename = "output.wav"
        audio_path = os.path.join(os.path.dirname(__file__), '../web/audio', audio_filename)

        print("Saving TTS to file: " + audio_path)
        
        self.text = text
        self.stream.feed(text)
        self.stream.play(muted=False, output_wavfile=audio_path)

        update_web_display(text, audio_filename)