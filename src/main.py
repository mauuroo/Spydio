import time
import lib as lb
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import keyboard

def main():
    user = lb.User(client_id=lb.CLIENT_ID, client_secret=lb.CLIENT_SECRET, redirect_uri=lb.REDIRECT_URI, scope=lb.SCOPE)
    state = True

    while True:
        if lb.get_audio.is_mute():
            if state:
                last_key = lb.last_key_pressed.get_last_key()
                print(last_key)
                if last_key not in ["left", "right"]:
                    user.start_playback()
                    state = False
        else:
            if not state:
                user.pause_playback()
                state = True

        time.sleep(0.2)
        
if __name__ == "__main__":
    main()

