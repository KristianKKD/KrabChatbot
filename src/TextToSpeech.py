from RealtimeTTS import TextToAudioStream, SystemEngine
import asyncio

class TextToSpeech:
    text = ""

    def __init__(self):
        print("Creating TTS instance")
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