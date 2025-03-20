import os
import sys
import customtkinter
from lib import spotify_config as sc, spotify_api as sa
from requests import get
from PIL import Image, ImageDraw
from io import BytesIO

def circular_img(image_url, size):
    response = get(image_url)
    img = Image.open(BytesIO(response.content)).resize((size, size), Image.LANCZOS)
    
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    
    circular_img = Image.new('RGBA', (size, size))
    circular_img.paste(img, (0, 0), mask=mask)
    
    return circular_img

def truncate_text(text, limit, truncate):
    if len(text) > limit:
        return text[:truncate] + "..."
    return text

def get_theme_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'src','assets', 'theme.json')
    else:
        return os.path.join('src', 'assets', 'theme.json')


customtkinter.set_default_color_theme(get_theme_path())
class MyFrame(customtkinter.CTkFrame):
    """
    Frame for the main screen of the application
    
    """
    def __init__(self, master, user, monitors, change_window,**kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1, uniform="col")
        self.grid_columnconfigure(1, weight=1, uniform="col")
        self.grid_columnconfigure(2, weight=1, uniform="col")

        self.is_playing = False
        self.mode = 1
        self.volume = 50
        self.monitor = None

        self.change_window = change_window

        #Frame for song data
        self.column2_border = customtkinter.CTkFrame(self, border_color="#f8f9fa", border_width=1, fg_color="transparent")

        self.column2_border.grid(row=0, column=2, rowspan=9, padx=10,pady=(10, 0),sticky="nsew")

        #Image
        logo_path =  logo_path = os.path.join(sys._MEIPASS, 'src','assets', 'spydio_logo.png') if getattr(sys, 'frozen', False) else "src/assets/spydio_logo.png"
        logo = customtkinter.CTkImage(dark_image=Image.open(logo_path), size=(110, 30))
        self.logo_label = customtkinter.CTkLabel(self, image=logo, text="")
        self.logo_label.grid(row=0, column=0, padx=10, pady=15, sticky="nw")

        #Switch
        self.switch_var = customtkinter.StringVar(value="off")
        self.switch = customtkinter.CTkSwitch(self, text="", command=self.change_credentials, variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch.grid(row=0, column=1, padx=10, pady=15, sticky="e")

        #Mode
        self.mode_label = customtkinter.CTkLabel(self, text="Mode")
        self.mode_label.grid(row=4, column=0, padx= 10, sticky="w")

        self.mode_combobox = customtkinter.CTkComboBox(self, values=["Play / Pause", "Volume Increase / Decrease"], command=self.get_mode)
        self.mode_combobox.grid(row=5, column=0, padx= 10, pady=(0, 20), sticky="w")

        #Monitor Configuration
        self.monitor_label = customtkinter.CTkLabel(self, text="Monitor")
        self.monitor_label.grid(row=4, column=1, padx=10, sticky="w")
        
        self.monitor_combobox = customtkinter.CTkComboBox(self, values=monitors, command=self.get_monitor)
        self.monitor_combobox.grid(row=5, column=1, padx=10, pady=(0, 20), sticky="w") 

        self.monitor_combobox.set(value=monitors[0])
        self.monitor = self.monitor_combobox.get()

        #Playback Style
        self.playback_label = customtkinter.CTkLabel(self, text="Playback Style")
        self.playback_label.grid(row=6, column=0, padx=10, sticky="w")

        self.playback_combobox = customtkinter.CTkComboBox(self, values=["Play Spotify", "Select Playlist"], command=self.get_playback)
        self.playback_combobox.grid(row=7, column=0, padx= 10, pady=(0, 20), sticky="w")

        #Playlist
        self.playlist_label = customtkinter.CTkLabel(self, text="Playlist ID")
        self.playlist_label.grid(row=6, column=1, padx=10, sticky="w")

        self.playlist_entry = customtkinter.CTkEntry(self, state="disabled", fg_color="#6c757d")
        self.playlist_entry.grid(row=7, column=1, padx= 10, pady=(0, 20), sticky="w")

        #User Profile
        user_name, images = user.get_user_information()
        circular_image = circular_img(images[0]["url"], 60)

        img_tk = customtkinter.CTkImage(dark_image=circular_image, size=(50, 50))

        self.user_image = customtkinter.CTkLabel(self, text="", image=img_tk)
        self.user_image.image = img_tk
        self.user_image.grid(row=9, column=0,padx=10, pady=10, sticky="w")

        self.name_label = customtkinter.CTkLabel(self, text=user_name)
        self.name_label.grid(row=9, column=0, padx=(80, 0), pady=10, sticky="nw")

        self.name_label = customtkinter.CTkLabel(self, text="", text_color="#6c757d", font=("Roboto", 13))
        self.name_label.grid(row=9, column=0, padx=(80, 0), pady=10, sticky="sw")

        #Current song
        current_song = user.get_current_playback()
        song_image = get(current_song["album_picture"])

        img_song_data = Image.open(BytesIO(song_image.content))

        img_song_tk = customtkinter.CTkImage(dark_image=img_song_data, size=(180, 180))

        self.song_image = customtkinter.CTkLabel(self, text="", image=img_song_tk)
        self.song_image.image = img_song_tk
        self.song_image.grid(row=0, rowspan=6, column=2, pady=(30, 0), sticky="n")

        self.song_label = customtkinter.CTkLabel(self, text="Song: " + truncate_text(current_song["song"], limit=19, truncate=16), width=100, anchor="w", text_color="#e9ecef", font=("Roboto", 15))
        self.song_label.grid(row=6, column=2, padx=(30, 0), sticky="w")

        self.artist_label = customtkinter.CTkLabel(self, text="Artist: " + truncate_text(current_song["artist"]["name"], limit=20, truncate=18), width=100, anchor="w", text_color="#e9ecef", font=("Roboto", 15))
        self.artist_label.grid(row=7, column=2, padx=(30, 0), sticky="w")

        self.album_label = customtkinter.CTkLabel(self, text="Album: " + truncate_text(current_song["album"], limit=18, truncate=15), width=100, anchor="w", text_color="#e9ecef", font=("Roboto", 15))
        self.album_label.grid(row=8, column=2, padx=(30, 0), pady=(0, 10), sticky="nw")

        #Volume control
        self.volume_label = customtkinter.CTkLabel(self, text="Volume", text_color="#e9ecef", font=("Roboto", 15))
        self.volume_label.grid(row=9, column=2, padx=(25, 0), pady=10, sticky="nw")

        self.volume_slider = customtkinter.CTkSlider(self, from_=0, to=100, command= self.volumeSlider)
        self.volume_slider.grid(row=9, column=2, padx=(25, 0), pady=10, sticky="sw")


        #Play button
        self.play_button = customtkinter.CTkButton(self, text="Play", command=self.play_callback)
        self.play_button.grid(row=10, column=1, pady=10)
    
    def update_info_song(self, new_song):
        """
        Update the information of the current song

        Args:
            new_song (dict): Dictionary with the information of the new song
        """
        song_image = get(new_song["album_picture"])
        img_song_data = Image.open(BytesIO(song_image.content))
        img_song_tk = customtkinter.CTkImage(dark_image=img_song_data, size=(180, 180))
        self.song_image.configure(image=img_song_tk)

        self.song_label.configure(text="Song: " + truncate_text(new_song["song"], limit=19, truncate=16))
        self.artist_label.configure(text="Artist: " + truncate_text(new_song["artist"]["name"], limit=21, truncate=19))
        self.album_label.configure(text="Album: " + truncate_text(new_song["album"], limit=18, truncate=15))
    
    def update_spotify_status(self, is_playing):
        """
        Updates the GUI to reflect whether Spotify is playing music or not.
        
        Args:
            is_playing (bool): Indicates whether Spotify is playing music. 
                                If True, the label text will update to "Listening to Spotify". 
                                If False, it will update to "Listening to Browser".
        """
        if is_playing:
            self.name_label.configure(text="Listening to Spotify")
        else:
            self.name_label.configure(text="Listening to Browser")

    def change_credentials(self):
        """
        Changes the Spotify credentials if the configuration switch is on.
        Closes the current window and opens a new credentials configuration window.
        """
        if self.switch_var.get() == "on":
            self.master.destroy()
            config_screen = ConfigurationScreen(on_valid_credentials_callback=self.change_window)
            config_screen.mainloop()

    def play_callback(self):
        """
        Changes the play button's state and updates its text and color based on whether music is playing or not.
        Also toggles the 'is_playing' value to switch between play and pause states.
        """
        if self.is_playing:
            self.play_button.configure(text="Play", fg_color="#1ED760")
        else:
            self.play_button.configure(text="Stop", fg_color="#f8f9fa")
        self.is_playing = not self.is_playing
    
    def get_mode(self, selected_mode):
        """
        Sets the operating mode of the program based on the user's selection.
    
        Args:
            selected_mode (str): The mode selected by the user. It can be "Play / Pause" or any other value. 
            If it's "Play / Pause", the mode is set to 1; otherwise, it's set to 2.
        """
        if selected_mode == "Play / Pause":
            self.mode = 1
        else:
            self.mode = 2
    
    def get_monitor(self, value):
        self.monitor = self.monitor_combobox.get()
    
    def get_playback(self, selected_playback):
        """
        Enables or disables the playlist entry based on the user's selection.
        
        Args:
            selected_playback (str): The playback style selected by the user.
            """
        if selected_playback == "Select Playlist":
            self.playlist_entry.configure(state="normal", fg_color="#f8f9fa")
        else:
            self.playlist_entry.configure(state="disabled", fg_color="#adb5bd")

    def get_playlist(self, context_uri):
        """
        Returns the playlist ID if the user has selected the "Select Playlist" option.
        
        Args:
            context_uri (str): The context URI of the playlist.
        """
        playlist = self.playlist_entry.get()
        if playlist[34:56] == context_uri:
            return None
        return playlist[34:56]
    
    def volumeSlider(self, value):
        self.volume = value

class App(customtkinter.CTk):
    """
    Parent class for the main application window.
    """
    def __init__(self, user, monitors, change_window):
        super().__init__()

        self.title("Setup")
        self.geometry("700x460")
        self.resizable(False, False)
        self.iconbitmap(os.path.join(sys._MEIPASS, 'src','assets', 'spydio_icon.ico') if getattr(sys, 'frozen', False) else "src/assets/spydio_icon.ico")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame = MyFrame(self, user, monitors, change_window=change_window)
        self.frame.grid(row=0, column=0, sticky="nsew")

class ConfigurationScreen(customtkinter.CTk):
    def __init__(self, on_valid_credentials_callback):
        super().__init__()

        self.title("Credentials")
        self.geometry("300x410")
        self.resizable(False, False)
        self.iconbitmap(os.path.join(sys._MEIPASS, 'src','assets', 'spydio_icon.ico') if getattr(sys, 'frozen', False) else "src/assets/spydio_icon.ico")

        self.client_id = ""
        self.client_secret = ""

        self.error_var = customtkinter.StringVar(value="")

        self.on_valid_credentials_callback = on_valid_credentials_callback

        #Image
        logo_path = os.path.join(sys._MEIPASS, 'src','assets', 'spydio_logo.png') if getattr(sys, 'frozen', False) else "src/assets/spydio_logo.png"
        logo = customtkinter.CTkImage(dark_image=Image.open(logo_path), size=(170, 46))
        self.logo_label = customtkinter.CTkLabel(self, image=logo, text="")
        self.logo_label.pack(padx=10, pady=(70, 30))

        #Credentials
        self.client_id_entry = customtkinter.CTkEntry(self, placeholder_text="Client ID")
        self.client_id_entry.pack(padx=10, pady=10)
        
        self.client_secret_entry = customtkinter.CTkEntry(self, placeholder_text="Client Secret")
        self.client_secret_entry.pack(padx=10, pady=10)

        self.button = customtkinter.CTkButton(self, text="Save", command=self.save_credentials)
        self.button.pack(padx=10, pady=10)

        #Error Label
        self.error_label = customtkinter.CTkLabel(self, textvariable=self.error_var, text_color="#dc3545")
        self.error_label.pack(padx=10, pady=10)

    def save_credentials(self):
        client_id = self.client_id_entry.get()
        client_secret = self.client_secret_entry.get()

        if client_id and client_secret:
            if len(client_id) == 32 or len(client_secret) == 32:
                token_path = os.path.join(sa.token_dir(), ".spotify_token_cache")
                if os.path.exists(token_path):
                    os.remove(token_path)
                sc.save_credentials(client_id, client_secret)
                self.destroy()
                
                self.on_valid_credentials_callback(client_id, client_secret)
            else:
                self.error_var.set("Invalid credentials")              
