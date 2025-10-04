import json
import websocket
import base64
import hashlib
import os
import socket
import textwrap

HOST = "localhost"
PORT = 4455

OBS_TEXT_SOURCE_NAME = "IncomingMessage"
OBS_USER_SOURCE_NAME = "IncomingUsername"

class OBSComms:
    def __init__(self):
        self.ws = websocket.create_connection(f"ws://{HOST}:{PORT}")
        self._auth()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def set_text(self, text, user):
        print("Sending request to change: " + OBS_TEXT_SOURCE_NAME + " to: " + text)

        text = self.insert_newlines(text, 30)
        user = self.insert_newlines(user, 30)

        text_request = {
            "op": 6,
            "d": {
                "requestType": "SetInputSettings",
                "requestId": "1",
                "requestData": {
                    "inputName": OBS_TEXT_SOURCE_NAME,
                    "inputSettings": {
                        "text": text
                    }
                }
            }
        }

        user_request = {
            "op": 6,
            "d": {
                "requestType": "SetInputSettings",
                "requestId": "2",
                "requestData": {
                    "inputName": OBS_USER_SOURCE_NAME,
                    "inputSettings": {
                        "text": user
                    }
                }
            }
        }

        self.ws.send(json.dumps(text_request))
        self.ws.send(json.dumps(user_request))

        self.sock.sendto(b"TextUpdated", (HOST, PORT)) #show text

    def hide_text(self):
        self.sock.sendto(b"TextTimedOut", (HOST, PORT))

    def insert_newlines(self, text, n):
        return '\n'.join(textwrap.wrap(text, width=n))

    def _auth(self):
        def _build_auth_string(salt, challenge):
            secret = base64.b64encode(
                hashlib.sha256(
                    (os.environ["OBS_WEBSOCKET_PASSWORD"] + salt).encode('utf-8')
                ).digest()
            )
            auth = base64.b64encode(
                hashlib.sha256(
                    secret + challenge.encode('utf-8')
                ).digest()
            ).decode('utf-8')
            return auth

        message = self.ws.recv()
        result = json.loads(message) 
        #server_version = result['d'].get('obsWebSocketVersion')
        auth = _build_auth_string(result['d']['authentication']['salt'], result['d']['authentication']['challenge'])

        payload = {
            "op": 1,
            "d": {
                "requestId": "AuthenticateKrabBot",
                "rpcVersion": 1,
                "authentication": auth,
                "eventSubscriptions": 1000 
            }
        }
        self.ws.send(json.dumps(payload))
        message = self.ws.recv()
        # Message Identified...or so we assume...probably good to check if this is empty or not.
        result = json.loads(message)
        print(result)
