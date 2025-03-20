import os
import json
import sys

def get_credentials_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(os.getenv('APPDATA'), 'Spydio', 'credentials.json')
    else:
        return os.path.join(os.getcwd(), 'credentials.json')

def load_credentials():
    credentials_path = get_credentials_path()
    if os.path.exists(credentials_path):
        with open(credentials_path, 'r') as file:
            return json.load(file)
    return None

def save_credentials(client_id, client_secret):
    credentials_path = get_credentials_path()
    os.makedirs(os.path.dirname(credentials_path), exist_ok=True)
    with open(credentials_path, 'w') as file:
        json.dump({'client_id': client_id, 'client_secret': client_secret}, file)

credentials = load_credentials()
if credentials:
    CLIENT_ID = credentials.get('client_id', '')
    CLIENT_SECRET = credentials.get('client_secret', '')
else:
    CLIENT_ID = ''
    CLIENT_SECRET = ''

REDIRECT_URI = 'http://127.0.0.1:8888/callback'
SCOPE = (
        'user-read-playback-state '
        'user-modify-playback-state '
        'user-read-currently-playing '
        'playlist-read-private '
        'playlist-read-collaborative '
        'playlist-modify-public '
        'playlist-modify-private '
        'user-library-read '
        'user-library-modify '
        'app-remote-control '
        'streaming'
    )