import customtkinter as ctk

def off():
    print("off")


#def state_button(state):
   # return "On" if state else "Off"
        

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

#Window
height_window = 720
width_window = 700
app = ctk.CTk()

app.title("Spydio")
app.geometry(f"{height_window}x{width_window}")

my_entry = ctk.CTkEntry(app, placeholder_text="Enter your Client ID", text_color="6a6e73")
my_entry.pack(pady=(340, 10))

power_button = ctk.CTkButton(app, width=100, height=45, text="Play", command=off, fg_color="#b298dc", hover_color="#a663cc", corner_radius=20, state= "normal")
power_button.pack(pady=(0, 10))


#Mainloop
app.mainloop()