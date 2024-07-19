import spotipy
from spotipy.oauth2 import SpotifyOAuth


class User:
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        """
        Args:
            client_id: Client ID from Spotify for Developers
            client_secret: Client Secret from Spotify for Developers
            redirect_uri: Redirect URI from Spotify for Developers
            scope: permissions allowed to the program to work with spotify
        """
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                                client_id= client_id,
                                client_secret= client_secret,
                                redirect_uri= redirect_uri,
                                scope= scope
                                ))
    
    @staticmethod
    def get_current_playback(self):
        """
        Extracts the information of the currently playing song

        Args:
            
        """
        playback_info = self.sp.current_playback()
        return {
            "song": playback_info["item"]["name"],
            "artist": playback_info["item"]["artists"][0],
            "album": playback_info["item"]["album"]["name"],
            "album_picture": playback_info["item"]["album"]["images"][0]["url"]
        }

    def start_playback(self):
        self.sp.start_playback()
        self.unmute()
    
    def pause_playback(self):
        self.sp.pause_playback()
        self.mute()
    
    def unmute(self):
        for i in range(25, 75, 6):
            self.sp.volume(i)

    def mute(self):
        for i in range(75, 0, -6):
            self.sp.volume(i)    
    