import time
import lib as lb
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def main():
    user = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= lb.spotify_config.CLIENT_ID,
                                                     client_secret= lb.spotify_config.CLIENT_SECRET,
                                                     redirect_uri= lb.spotify_config.REDIRECT_URI,
                                                     scope= lb.spotify_config.SCOPE
                                                     ))
    
    # if lb.get_audio.is_mute():
    #     user.start_playback()
    # else:
    #     user.pause_playback()
    
    playback_info = user.current_playback()

    song_name = playback_info["item"]["name"]
    artist_name = playback_info["item"]["artists"][0]["name"]
    album_name = playback_info["item"]["album"]["name"]
    album_picture = playback_info["item"]["album"]["images"][0]["url"]

    user.volume(0)
    time.sleep(10)
    for i in range(25, 75, 6):
        user.volume(i)
    
    time.sleep(3)

    for i in range(75 , 0, -6):
        print(i)
        user.volume(i)
    

if __name__ == "__main__":
    main()

