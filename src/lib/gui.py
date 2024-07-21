import customtkinter as ctk

spotify_green = "#1DB954"
spotify_black = "#191414"
spotify_white = "#FFFFFF"
spotify_gray = "#B3B3B3"
def off():
    print("off")
    lng.configure(text = "Listening to spotify")


#def state_button(state):
   # return "On" if state else "Off"
        

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

#Window
height_window = 1600
width_window = 1095
app = ctk.CTk()

app.title("Spydio")
app.geometry(f"{height_window}x{width_window}")

client_id = ctk.CTkEntry(app, placeholder_text="Enter your Client ID", text_color = spotify_gray )
client_id.pack(pady=(340, 1))

client_key = ctk.CTkEntry(app, placeholder_text="Enter your Client Key", text_color = spotify_gray )
client_key.pack(pady=(240, 10))

playlist_id = ctk.CTkEntry(app, placeholder_text = "Playlist ID", text_color = spotify_gray )
playlist_id.pack(pady = (50 , 10))

lng = ctk.CTkLabel(app , text = "")
lng.pack(pady = (100,10))

power_button = ctk.CTkButton(app, width=100, height=45, text="Play", command=off, fg_color = spotify_green, hover_color = spotify_gray, corner_radius = 20, state = "normal" ,)
power_button.pack(pady=(0, 10))


#Mainloop
app.mainloop()