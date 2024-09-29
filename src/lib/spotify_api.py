import spotipy
from spotipy.oauth2 import SpotifyOAuth
from platform import node


class User:
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        """
        Args:
            client_id(str): Client ID from Spotify for Developers
            client_secret(str): Client Secret from Spotify for Developers
            redirect_uri(str): Redirect URI from Spotify for Developers
            scope(str): permissions allowed to the program to work with spotify
        """
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                                client_id= client_id,
                                client_secret= client_secret,
                                redirect_uri= redirect_uri,
                                scope= scope
                                ))
    
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
            dict: {"song": song, "artist": artist, "album": album, "album_picture": album_picture}
        """
        playback_info = self.sp.current_playback()
        return {
            "song": playback_info["item"]["name"],
            "artist": playback_info["item"]["artists"][0],
            "album": playback_info["item"]["album"]["name"],
            "album_picture": playback_info["item"]["album"]["images"][0]["url"]
        }

    def start_playback(self, limit, volumen, playlist_id = None):
        """
        Plays a specific playlist if specified; otherwise, only Spotify is played.

        Args:
            playlist_id(str): Playlist ID
        """

        try:
            self.sp.start_playback(context_uri=f"spotify:playlist:{playlist_id}" if playlist_id else None)
            self.increase(limit, volumen)
        except:
            self.force_playback()
    
    def pause_playback(self, volumen, limit):
        self.decrease(volumen, limit)
        self.sp.pause_playback()
    
    def increase(self, limit, volumen, step=9):
        """
        Progressively increases the volume until it reaches the desired level.

        Args:
            step (int): The step value to increase the volume. For example, 3 will increase the volume by 3 units at each step.
        """
        for i in range(limit, volumen, step):
            self.sp.volume(i)

    def decrease(self, volumen, limit, step=-9):
        """
        Progressively decreases the volume until limit.

        Args:
            step (int): The negative step value to decrease the volume. For example, -3 will decrease the volume by 3 units at each step.
        """
        for i in range(volumen, limit, step):
            self.sp.volume(i)    
    
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
        Forces playback to start on the computer device.
        """
        computer_name = node()
        devices = self.sp.devices()["devices"]
        for device in devices:
            if device["name"] == computer_name:
                self.sp.transfer_playback(device_id=device["id"], force_play=True)