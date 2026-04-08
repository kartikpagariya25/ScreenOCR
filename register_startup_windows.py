import os
import sys
import winreg


def register_startup() -> None:
    script_path = os.path.abspath("screen_ocr.py")
    pythonw = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    if not os.path.exists(pythonw):
        pythonw = sys.executable

    command = f'"{pythonw}" "{script_path}"'

    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        0,
        winreg.KEY_SET_VALUE,
    )

    try:
        winreg.SetValueEx(key, "ScreenOCR", 0, winreg.REG_SZ, command)
    finally:
        winreg.CloseKey(key)

    print("Startup entry added: ScreenOCR")


def unregister_startup() -> None:
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        0,
        winreg.KEY_SET_VALUE,
    )

    try:
        try:
            winreg.DeleteValue(key, "ScreenOCR")
            print("Startup entry removed: ScreenOCR")
        except FileNotFoundError:
            print("Startup entry does not exist.")
    finally:
        winreg.CloseKey(key)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "remove":
        unregister_startup()
    else:
        register_startup()
