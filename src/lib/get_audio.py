from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

def is_any_browser_playing_audio(browser_names=(
    "chrome.exe", "firefox.exe", "msedge.exe", "iexplore.exe", "opera.exe",
    "vivaldi.exe", "brave.exe", "chromium.exe", "safari.exe", "maxthon.exe",
    "yandex.exe", "palemoon.exe", "waterfox.exe", "seamonkey.exe", "avant.exe",
    "tor.exe", "epic.exe", "slimjet.exe", "midori.exe", "comodo_dragon.exe"
)):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process:
            process_name = session.Process.name().lower()
            if process_name in (name.lower() for name in browser_names):
                try:
                    volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                    if volume.GetMasterVolume() > 0:
                        return True
                except Exception as e:
                    print(f"Error al consultar el volumen para {process_name}: {e}")

    return False

# Ejemplo de uso
if __name__ == "__main__":
    if is_any_browser_playing_audio():
        print("Alguno de los navegadores está reproduciendo audio.")
    else:
        print("Ninguno de los navegadores está reproduciendo audio.")


