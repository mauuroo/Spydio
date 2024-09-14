import time
import lib as lb
from psutil import process_iter
import subprocess

def is_spotify_running():
    """
    Checks if Spotify is currently running.

    Returns:
        bool: True if Spotify is running, False otherwise.
    """

    for proc in process_iter(['name']):
        if proc.info["name"] == "Spotify.exe":  # For Windows
            return True
        elif proc.info["name"] == "Spotify":  # For macOS and Linux
            return True
    return False    



def main():
    user = lb.User(client_id=lb.CLIENT_ID, client_secret=lb.CLIENT_SECRET, redirect_uri=lb.REDIRECT_URI, scope=lb.SCOPE)
    state = True

    #Makes sure to have spotify open for the correct execution of the program
    if not is_spotify_running():
        subprocess.Popen("spotify")
        time.sleep(10)

    try:
        click_detector = lb.on_click_allowed.ClickDetector()
        click_detector.select_monitor()

        while True: 
            if lb.get_audio.is_mute():
                if state:
                    last_key = lb.last_key_pressed.get_last_key()
                    if  click_detector.has_left_clicked():
                        if click_detector.approximate_pause_click_in_monitor():
                            user.start_playback()  
                            state = False
                    elif last_key not in ["left", "right"]:
                        user.start_playback()
                        state = False
            else:
                if not state:
                    user.pause_playback()
                    state = True

            time.sleep(0.25)


    finally:
        click_detector.stop()
            
if __name__ == "__main__": 
    main()