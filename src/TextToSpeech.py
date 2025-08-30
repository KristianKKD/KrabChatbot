import os
#from RealtimeTTS import TextToAudioStream, ZipVoiceEngine, ZipVoiceVoice
from RealtimeTTS import TextToAudioStream, SystemEngine
import asyncio
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

class TextToSpeech:
    text = ""

    def __init__(self):
        print("Creating TTS instance")
        # zipvoice_root = r"E:\AI\models\ZipVoice"

        # voice_1 = ZipVoiceVoice(
        #     prompt_wav_path=os.path.join(zipvoice_root, "zipvoice_reference1.wav"),
        #     prompt_text="Hello there! I'm really excited to try this out! I hope the speech sounds natural and warm - that's exactly what I'm going for!"
        # )

        # self.engine = ZipVoiceEngine(zipvoice_root=zipvoice_root, voice=voice_1, model_name="zipvoice")
        # self.stream = TextToAudioStream(self.engine)
        self.engine = SystemEngine()
        self.stream = TextToAudioStream(self.engine)

    def __del__(self):
        #print("Deleting TTS instance")
        self.stream.stop()

    async def speak(self, text, prefix = "Speaking text: "):
        print(prefix + text)
        self.text = text
        self.stream.feed(text)
        await asyncio.to_thread(self.stream.play)

    def stop(self):
        print("Stopping TTS message: " + self.text)
        self.stream.stop()