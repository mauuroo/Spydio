import time
import lib as lb

def main():
    user = lb.User(client_id=lb.CLIENT_ID, client_secret=lb.CLIENT_SECRET, redirect_uri=lb.REDIRECT_URI, scope=lb.SCOPE)
    state = True


    try:
        click_detector = lb.on_click_allowed.ClickDetector()
            
        while True:
            if lb.get_audio.is_mute():
                if state:
                    last_key = lb.last_key_pressed.get_last_key()
                    if last_key not in ["left", "right"]:
                        if click_detector.has_left_clicked():
                            x, y = click_detector.left_click_coordinates
                            if x <= 3840 and y <= 2160:
                                user.start_playback()
                                state = False
                        else:
                            user.start_playback()
                            state = False
            else:
                if not state:
                    user.pause_playback()
                    state = True

            time.sleep(0.2)


    finally:
        click_detector.stop()
            
if __name__ == "__main__":
    main()
