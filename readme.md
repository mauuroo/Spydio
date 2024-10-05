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

## Tutorial
> **Note:** The graphical interface for Spydio will not be available until January 2025. Therefore, all interactions with the program must be done through the console.


### 1. Cloning the Repository
To get started, clone the repository to your local machine. You can do this by running the following command:

```bash
git clone https://github.com/mauuroo/Spydio.git
```
### 2. Installing Dependencies
Navigate into the project directory:
```bash
cd Spydio
```
Install the required dependencies. You can do this using:
```bash
pip install -r requirements.txt
```
### 3. Spotify Account Configuration
You must set up your Spotify credentials so that Spydio can interact with your account. Follow these steps:

1. Log in to your Spotify account:
   - Go to the [Spotify for Developers](https://developer.spotify.com) page and log in.

2. Access the Dashboard:
   - Once logged in, click on "Dashboard" at the top of the page or go directly to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).

3. Create a New Application:
   - In the dashboard, click on **"Create an App"**.
   - Fill in the required fields (name, description) and agree to the terms.
   - Once the application is created, you will see your **client_id** and **client_secret**.

4. Configure Spydio:
   - Open the `spotify_config.py` file in the project.
   - Replace the placeholder values with your credentials:
   ```python
   CLIENT_ID='your_client_id'
   CLIENT_SECRET='your_client_secret'
### 4. Run the program
Being in the program directory executes:
```bash
python main.py
```
When running, the program will ask for certain information through the console before starting. Once set up, it will run in the background, pausing and resuming your Spotify playback based on browser activity.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.