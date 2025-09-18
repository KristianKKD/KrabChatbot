import requests
import os

def update_web_display(text, audio_filename):
    url = os.environ.get('WEB_DISPLAY_URL', 'http://localhost:5000/update')
    payload = {'text': text, 'audio': audio_filename}
    try:
        response = requests.post(url, json=payload, timeout=2)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to update web display: {e}")
