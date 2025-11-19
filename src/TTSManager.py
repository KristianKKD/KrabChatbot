import os
from RealtimeTTS import TextToAudioStream
#from RealtimeTTS import AzureEngine
from RealtimeTTS import SystemEngine
import asyncio
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
#import random

class TextToSpeech:
    text : str
    id : int

    def __init__(self, id):
        print("Creating TTS instance")
        #self.engine = AzureEngine(speech_key=os.environ["AZURE_SPEECH_KEY"], service_region="uksouth")
        self.engine = SystemEngine()

        self.stream = TextToAudioStream(self.engine)

        #print(self.stream.engine.get_voices())

        #self.stream.engine.set_voice("LolaNeural")
        #self.stream.engine.set_voice("FlorianMultilingualNeural")

        self.id = id

    def __del__(self):
        #print("Deleting TTS instance")
        self.stream.stop()

    async def speak(self, text, user = "", discord_bot = None, obs_comms = None):
        print(user + " said:" + text)
        self.text = text
        self.stream.feed(text)

        #voices = self.stream.engine.get_voices()
        #random_index = random.randint(0, len(voices) - 1)
        #self.stream.engine.set_voice(voices[random_index])

        audio_filename = "output" + str(self.id) + ".wav"
        audio_path = os.path.join(os.getcwd(), 'audio', audio_filename)

        if obs_comms is not None:
            obs_comms.set_text(text, user)

        if discord_bot is not None:
            await asyncio.to_thread(self.stream.play, output_wavfile=audio_path, muted=True)
            await discord_bot.queue_play(audio_path)
        else:
            await asyncio.to_thread(self.stream.play, output_wavfile=audio_path)

        if obs_comms is not None:
            obs_comms.hide_text()

    def stop(self):
        print("Stopping TTS message: " + self.text)
        self.stream.stop()
