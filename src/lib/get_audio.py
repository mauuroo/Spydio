from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioMeterInformation
def is_mute(browser_names=(
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
                meter_info = session._ctl.QueryInterface(IAudioMeterInformation)
                peak = meter_info.GetPeakValue()
                print(f"Process: {process_name}, Volume: {peak}")
                if peak == 0:
                    return True
    return False




