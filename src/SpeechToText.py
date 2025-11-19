from io import BytesIO
import os
import asyncio
import warnings
from dotenv import load_dotenv


from elevenlabs.client import ElevenLabs

warnings.filterwarnings("ignore", category=FutureWarning)


from pynput import keyboard
import pyaudio
import wave

class RecordAudio():
    recording : bool

    channels = 1
    rate = 44100
    format = pyaudio.paInt16

    def __init__(self, audio_path):
        self.recording = False
        self.p = pyaudio.PyAudio()
        self.audio_path = audio_path
        
    def start_recording(self):
        if self.recording: 
            return
        
        try:
            self.frames = []
            self.stream = self.p.open(format=self.format,
                            channels=self.channels,
                            rate=self.rate,
                            input=True,
                            frames_per_buffer=8192,
                            stream_callback=self.recording_callback)
            
            print("Stream active:", self.stream.is_active())
            print("start Stream")
            self.recording = True
        except:
            raise

    def recording_callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return in_data, pyaudio.paContinue
    
    def stop_recording(self):
        if not self.recording: 
            return
        
        self.recording = False
        
        print("Stop recording")
        self.stream.stop_stream()
        self.stream.close()

        with wave.open(self.audio_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))

class SpeechToText(keyboard.Listener):
    text : str
    model_id : str
    recording_key = 'r'
    audio_recorder : RecordAudio

    def __init__(self, api_key, model_id=""):
        print("Creating Speech To Text instance")

        super(SpeechToText, self).__init__(self.on_press, self.on_release)

        audio_filename = "input.wav"
        audio_path = os.path.join(os.getcwd(), 'audio', audio_filename)

        self.recorder = RecordAudio(audio_path)

        self.model_id = model_id
        if model_id == "":
            self.model_id = "scribe_v1"

        self.elevenlabs = ElevenLabs(
            api_key=api_key,
        )

    def on_press(self, key):
        if key.char == self.recording_key:
            self.recorder.start_recording()
        return True

    def on_release(self, key):
        if key.char == self.recording_key:
            self.recorder.stop_recording()
            asyncio.run(self.get_transcription(self.recorder.audio_path))
            return True
        
        print("KEY FAILED?")
        return False

    def __del__(self):
        print("Deleting Speech to Text instance")
        return

    async def get_transcription(self, audio_path):
        print("Getting transcription...")

        audio_data = BytesIO(open(audio_path, "rb").read())

        transcription = self.elevenlabs.speech_to_text.convert(
            file=audio_data,
            model_id=self.model_id, # Model to use
            tag_audio_events=True, # Tag audio events like laughter, applause, etc.
            language_code="eng", # Language of the audio file. If set to None, the model will detect the language automatically.
            diarize=True, # Whether to annotate who is speaking
        )

        print(transcription.text)