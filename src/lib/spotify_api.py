import spotipy
import requests
from os import path, makedirs
from spotipy.oauth2 import SpotifyOAuth
from platform import node
from time import sleep

def token_dir():
    TOKEN_DIR = path.join(path.expanduser("~"), ".spydio")
    makedirs(TOKEN_DIR, exist_ok=True)

    return TOKEN_DIR
class User:
    def __init__(self, client_id, client_secret, redirect_uri, scope, on_valid_credentials_callback):
        """
        Args:
            client_id(str): Client ID from Spotify for Developers
            client_secret(str): Client Secret from Spotify for Developers
            redirect_uri(str): Redirect URI from Spotify for Developers
            scope(str): permissions allowed to the program to work with spotify
        """
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                                    client_id=client_id,
                                    client_secret=client_secret,
                                    redirect_uri=redirect_uri,
                                    scope=scope,
                                    cache_path=path.join(token_dir(), ".spotify_token_cache")
                                ))

        self.is_token_valid = self.validate_token(client_id, client_secret)

        if self.is_token_valid:
            self.client_id = self.get_device()
        else:
            from lib.gui import ConfigurationScreen
            configuration_screen = ConfigurationScreen(on_valid_credentials_callback=on_valid_credentials_callback)
            configuration_screen.mainloop()

    def validate_token(self, client_id, client_secret):
        """
        Validates the token by sending a request to the Spotify API.

        Args:
            client_id(str): Client ID from Spotify for Developers
            client_secret(str): Client Secret from Spotify for Developers
        
        Returns:
            bool: True if the token is valid, False otherwise.
        """
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            return True
        return False

    def get_device(self):
        """
        Returns the ID of the device where the program is running
        """
        try:
            computer_name = node()
            devices = self.sp.devices()["devices"]
            for device in devices:
                if device["name"] == computer_name:
                    return device["id"]
        except spotipy.exceptions.SpotifyException:
            self.on_valid_credentials_callback()
    def get_user_information(self):
        """
        Returns the user's name and profile picture
        """
        user_info = self.sp.current_user()
        return user_info["display_name"], user_info["images"]
    

    def get_current_playback(self):
        """
        Extracts the information of the currently playing song

        Return:
            dict: {"song": song, "artist": artist, "album": album, "album_picture": album_picture, "uri": uri}
        """
        playback_info = self.sp.current_playback()

        return {
            "song": playback_info["item"]["name"],
            "artist": playback_info["item"]["artists"][0],
            "album": playback_info["item"]["album"]["name"],
            "album_picture": playback_info["item"]["album"]["images"][0]["url"],
            "uri": playback_info.get("context", {}).get("uri", None)[17:] if playback_info.get("context") and playback_info["context"].get("uri") else None,
        }



    def start_playback(self, volumen=100, playlist_id = None):
        """
        Plays a specific playlist if specified; otherwise, only Spotify is played.

        Args:
            playlist_id(str): Playlist ID
        """
        self.sp.start_playback(device_id=self.client_id, context_uri=f"spotify:playlist:{playlist_id}" if playlist_id else None)
        self.increase(volumen)
    
    def pause_playback(self, volumen):
        self.decrease(volumen)
        self.sp.pause_playback(device_id=self.client_id)
    
    def increase(self, volumen, pct=0.3, cof=5):
        """
        Progressively increases the volume until it reaches the desired level.

        Args:
            step (int): The step value to increase the volume. For example, 3 will increase the volume by 3 units at each step.
        """
        for i in range(int(volumen * pct), (int(volumen * pct) +  int(volumen * 0.14) * cof), int(volumen*0.14)):
            self.sp.volume(i, device_id=self.client_id)
        self.sp.volume(i + int(volumen*0.14), device_id=self.client_id)

    def decrease(self, volumen, pct=0.3, cof=5):
        """
        Progressively decreases the volume until limit.

        Args:
            step (int): The negative step value to decrease the volume. For example, -3 will decrease the volume by 3 units at each step.
        """
        for i in range((int(volumen * pct) +  int(volumen * 0.14) * cof), int(volumen * pct), -int(volumen*0.14)):
            self.sp.volume(i, device_id=self.client_id)
        self.sp.volume(i - int(volumen*0.14), device_id=self.client_id)
    
    def get_playlist(self):
        """
        Retrieves the current user's playlists and their basic information.

        Returns:
            list of dict: A list of dictionaries, each containing:
                - name (str): The name of the playlist.
                - id (str): The Spotify ID of the playlist.
                - tracks (int): The total number of tracks in the playlist.
        """
        playlists = self.sp.current_user_playlists()
        playlist_info = list()

        for playlist in playlists["items"]:
            playlist_info.append({
                "name": playlist["name"],
                "id": playlist["id"],
                "tracks": playlist["tracks"]["total"]
            })
        return playlist_info
    
    def force_playback(self):
        """
        Forces the playback to start and pause immediately.
        """

        try:
            if not self.sp.current_playback()["is_playing"]:
                self.sp.volume(0, device_id=self.client_id)
                self.sp.start_playback(device_id=self.client_id)
                sleep(1)

            self.sp.pause_playback(device_id=self.client_id)
            self.sp.volume(15, device_id=self.client_id)
        except Exception:
            self.sp.volume(0, device_id=self.client_id)
            self.sp.start_playback(device_id=self.client_id)
            sleep(1)
            self.sp.pause_playback(device_id=self.client_id)