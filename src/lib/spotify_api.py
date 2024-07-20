import spotipy
from spotipy.oauth2 import SpotifyOAuth


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

    def start_playback(self, playlist_id=None, step=6):
        """
        Plays a specific playlist if specified; otherwise, only Spotify is played.

        Args:
            playlist_id(str): Playlist ID
        """

        if playlist_id:
            self.sp.start_playback(context_uri=f"spotify:playlist:{playlist_id}")
        else:
            self.sp.start_playback()
        self.unmute(step)
    
    def pause_playback(self, step=-6):
        self.mute(step)
        self.sp.pause_playback()
    
    def unmute(self, step):
        """
        Progressively increases the volume until it reaches the desired level.

        Args:
            step (int): The step value to increase the volume. For example, 3 will increase the volume by 3 units at each step.
        """
        for i in range(55, 75, step):
            self.sp.volume(i)

    def mute(self, step):
        """
        Progressively decreases the volume until muted.

        Args:
            step (int): The negative step value to decrease the volume. For example, -3 will decrease the volume by 3 units at each step.
        """
        for i in range(75, 0, step):
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