import requests

MODEL_SERVER_URL = "http://192.168.1.232:5000"
MAX_CONTEXT_MESSAGES = 20
context = []

def generate_response(prompt):
    url = f"{MODEL_SERVER_URL}/generate"
    response_context = context[-MAX_CONTEXT_MESSAGES:]

    try:
        payload = {
            "prompt": prompt,
            "context": response_context
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        print(f"Model server error: {e}")
        return "Sorry, I couldn't get a response from the model."

def add_to_context(user, content):
    entry = user + ":" + content + "\n"
    context.append(entry)
    if len(context) > MAX_CONTEXT_MESSAGES:
        context.pop(0)  # remove oldest

def clear_context():
    context.clear()

def restart_model():
    url = f"{MODEL_SERVER_URL}/restart"
    
    try:
        response = requests.post(url)
        response.raise_for_status()
        return response.json().get("status", "Unknown")
    except Exception as e:
        print(f"Model server restart error: {e}")
        return "Failed to restart the model."