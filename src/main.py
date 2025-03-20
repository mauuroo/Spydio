import time
import lib as lb
from psutil import process_iter
import subprocess
import threading

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

def play_mode(user, mode, volumen, playlist):

        if mode == 1:
            if not user.sp.current_playback()["is_playing"]:
                user.start_playback(volumen=volumen, playlist_id=playlist)
        else:
            user.increase(volumen=volumen, pct=0.44, cof=4)
        return False

def main():
    """
    The main function that runs the program.

    This function ensures that Spotify is running, attempts to authenticate the user using stored credentials,
    and initializes the main program logic and graphical user interface (GUI). If credentials are missing,
    it opens a configuration screen for the user to enter them.

    Steps:
        1. Check if Spotify is running. If not, open Spotify.
        2. Attempt to authenticate the user using predefined client ID and secret.
        3. If credentials are present, start the main program by initializing the user and GUI, and then
           begin the main program logic in a separate thread.
        4. If credentials are missing, prompt the user to enter valid credentials via the configuration screen.
    """
    def start_main_program(client_id, client_secret):
        user = lb.User(client_id=client_id, client_secret=client_secret, redirect_uri=lb.REDIRECT_URI, scope=lb.SCOPE, on_valid_credentials_callback=start_main_program)
        user.force_playback()
        monitors = list()
        monitors = [f"{monitor['name']} | {monitor['width']}x{monitor['height']} | Primary: {monitor['is_primary']}" for monitor in  lb.on_click_allowed.ClickDetector.get_info_monitors()]

        gui = lb.App(user=user, monitors=monitors, change_window=start_main_program)
        update_thread = threading.Thread(target=main_logic, args= (user, gui,), daemon=True)
        update_thread.start()

        gui.mainloop()


    #Makes sure to have spotify open for the correct execution of the program
    if not is_spotify_running():
        subprocess.Popen("spotify")
        time.sleep(10)

    if lb.CLIENT_ID != "" and lb.CLIENT_SECRET != "":
        start_main_program(client_id=lb.CLIENT_ID, client_secret=lb.CLIENT_SECRET)
    else:
        config_screen = lb.ConfigurationScreen(on_valid_credentials_callback=start_main_program)
        config_screen.mainloop()

def main_logic(user, gui):
    """
    The main loop that continuously checks and updates the playback state, volume, and user interactions.

    This loop controls the core playback logic, including adjusting volume, monitoring click events, handling 
    mute states, and updating the playback status based on user interactions and the current playback state.

    Flow:
        - If the user is playing music, the program tracks the volume, song, and playback mode.
        - The volume is adjusted based on the current mode and user input.
        - If the system detects that the audio is muted, it waits for the user to interact (via mouse click or keyboard press) 
          to toggle the playback state.
        - The loop continuously checks for updates to the current song and adjusts playback accordingly.
    """
    while True:
        if gui.frame.is_playing:
            state = True
            volumen = int(gui.frame.volume)
            previus_song = None
            previus_volume = volumen
            previus_mode = int(gui.frame.mode)
            context_uri = None

            if gui.frame.mode == 2:
                if not user.sp.current_playback()["is_playing"]:
                    user.start_playback(volumen=int(volumen * 0.44), playlist_id=gui.frame.get_playlist(context_uri=context_uri))
            
            try:
                click_detector = lb.on_click_allowed.ClickDetector()
                click_detector.select_monitor(gui.frame.monitor)
                new_click = None

                while gui.frame.is_playing:

                    if previus_volume != int(gui.frame.volume):
                        volumen = int(gui.frame.volume)
                        previus_volume = volumen

                        #Control for the slider
                        if state:
                            if gui.frame.mode == 1:
                                user.sp.volume(int(volumen * 0.3), device_id=user.client_id)
                            else:
                                user.sp.volume(int(volumen * 0.44), device_id=user.client_id)
                        else:
                            user.sp.volume(volumen, device_id=user.client_id)
    
                    if lb.get_audio.is_mute(): 
                        if state: 
                            last_key = lb.last_key_pressed.get_last_key()

                            if new_click != click_detector.left_click_coordinates:
                                new_click = click_detector.left_click_coordinates

                                if click_detector.approximate_pause_click_in_monitor(): 
                                    state = play_mode(user, gui.frame.mode, volumen, playlist=gui.frame.get_playlist(context_uri=context_uri))

                            elif last_key == "space":
                                state = play_mode(user, gui.frame.mode, volumen, playlist=gui.frame.get_playlist(context_uri=context_uri))

                        if previus_mode != gui.frame.mode:
                            previus_mode = gui.frame.mode
                    else:
                        if not state:
                            if gui.frame.mode == 1:
                                user.pause_playback(volumen=volumen)
                            else:
                                user.decrease(volumen=volumen, pct=0.44, cof=4)
                            state = True
                        
                        if previus_mode != gui.frame.mode:
                            if gui.frame.mode == 1:
                                user.pause_playback(volumen=int(volumen * 0.3))
                            else:
                                user.start_playback(volumen=int(volumen * 0.3), playlist_id=gui.frame.get_playlist(context_uri=context_uri))
                            previus_mode = gui.frame.mode


                    actual_song = user.get_current_playback()
                    if actual_song != previus_song:
                        gui.frame.update_info_song(actual_song)
                        previus_song = actual_song
                        context_uri = actual_song["uri"]

                    if user.sp.current_playback()["is_playing"]:
                        gui.frame.update_spotify_status(True)
                    else:
                        gui.frame.update_spotify_status(False)
                    
                    time.sleep(0.25)


            finally:
                click_detector.stop()
        else:
            time.sleep(1)


if __name__ == "__main__":
    main()