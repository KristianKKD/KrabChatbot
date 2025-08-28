from RealtimeTTS import TextToAudioStream, SystemEngine

class TextToSpeech:
    def __init__(self):
        self.engine = SystemEngine()  # Replace with your TTS engine if needed
        self.stream = TextToAudioStream(self.engine)
        self.last_text = None

    def speak(self, text):
        self.last_text = text
        self.stream.feed(text)
        self.stream.play_async()

    def stop(self):
        self.stream.stop()

    def replay_last(self):
        if self.last_text:
            self.stop()
            self.stream.feed(self.last_text)
            self.stream.play_async()