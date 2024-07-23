# Spydio

Spydio is a tool designed to manage Spotify playback based on the audio state of other programs, such as a web browser. If the audio from the browser is paused or muted, Spydio can resume playback on Spotify, and vice versa.

## Features

- Detects if the browser is playing audio.
- Pauses or resumes Spotify playback based on the browser's audio state.
- Allows monitor configuration and detection of clicks in specific areas.
- Compatible with multiple browsers and monitors.

## Requirements

- Python 3.12 or higher
- Python libraries:
  - `spotipy` for interacting with the Spotify API.
  - `pynput` for detecting keyboard and mouse clicks.
  - `PyQt5` for monitor detection and handling.
  - `customtkinter` for the graphical user interface.
  
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
