# Spydio (**sp**: <ins>sp</ins>otify, **py**: <ins>py</ins>thon, **dio**: au<ins>dio</ins>)


Spydio is a tool designed to manage Spotify playback based on the audio status of other applications, such as a web browser. If the browser's audio is paused or muted, Spydio will automatically resume playback on Spotify, eliminating the need to manually control it through the application. Likewise, when audio is resumed or sound is detected again in the browser, Spydio will automatically pause Spotify playback.

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
