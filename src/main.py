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

def play_mode(user, mode, limit, volumen):
    if mode == 1:
        user.start_playback(limit=limit, volumen=volumen)
    else:
        user.increase(limit=limit, volumen=volumen) 
    return False



def main():
    user = lb.User(client_id=lb.CLIENT_ID, client_secret=lb.CLIENT_SECRET, redirect_uri=lb.REDIRECT_URI, scope=lb.SCOPE)
    state = True

    #Makes sure to have spotify open for the correct execution of the program
    if not is_spotify_running():
        subprocess.Popen("spotify")
        time.sleep(10)

    mode = int(input("Seleccionar modo: \n"
                     "1) Reproducir / Pausar \n"
                     "2) Disminución del volumen \n"))
    
    volumen = int(input("Ingrese Nivel de Volumen [0 - 100]: "))
    limit = user.volumen_calibrate(volumen, mode)
    
    try:
        click_detector = lb.on_click_allowed.ClickDetector()
        click_detector.select_monitor()
        new_click = None

        while True:  
            if lb.get_audio.is_mute(): 
                if state: 
                    last_key = lb.last_key_pressed.get_last_key()

                    if new_click != click_detector.left_click_coordinates:
                        new_click = click_detector.left_click_coordinates

                        if click_detector.approximate_pause_click_in_monitor(): 
                            state = play_mode(user, mode, limit, volumen)

                    elif last_key == "space":
                        state = play_mode(user, mode, limit, volumen)
            else:
                if not state:
                    if mode == 1:
                        user.pause_playback(volumen=volumen, limit=limit)
                    else:
                        user.decrease(volumen=volumen, limit=limit)
                    state = True

            time.sleep(0.25)


    finally:
        click_detector.stop()
            
if __name__ == "__main__": 
    main()