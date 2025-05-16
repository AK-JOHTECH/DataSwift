import PySimpleGUI as sg
import subprocess
import os
import sys

# === Function to get path for bundled or development ===
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        base_path = sys._MEIPASS  # PyInstaller sets this
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# === Path to C++ executable ===
EXE_PATH = resource_path(r"C:\Users\akohli\Music\Cap Bridge\bridge\Debug\bridge.exe")  # If you put it in a folder, e.g., 'resources/bridge.exe'

# === GUI layout ===
layout = [
    [sg.Text("Capacitance (nF):"), sg.InputText("", key="CAP", size=(20, 1), readonly=True)],
    [sg.Text("Dissipation Factor:"), sg.InputText("", key="DF", size=(20, 1), readonly=True)],
    [sg.Button("Trigger"), sg.Button("Exit")]
]

# === Create window ===
window = sg.Window("Capacitance Reader", layout)

# === Main event loop ===
while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, "Exit"):
        break

    if event == "Trigger":
        try:
            result = subprocess.run([EXE_PATH], capture_output=True, text=True, timeout=10)
            output = result.stdout.strip().splitlines()

            cap = ""
            df = ""

            for line in output:
                if "Capacitance" in line:
                    cap = line.split(":")[1].strip().replace("pF", "").strip()
                elif "Dissipation Factor" in line:
                    df = line.split(":")[1].strip()

            if cap and df:
                window["CAP"].update(float(cap)*1000000000)
                window["DF"].update(df)
            else:
                sg.popup_error("Could not parse response:\n" + "\n".join(output))

        except Exception as e:
            sg.popup_error("Error calling bridge.exe", str(e))

# === Close window ===
window.close()
