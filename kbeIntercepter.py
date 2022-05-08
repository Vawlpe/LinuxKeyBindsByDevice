import os
import threading
import evdev


def RunShell(cmd, block):
    os.system(f"{cmd}{'' if block == 'True' else ' &'}")


def EventCheckLoop(kbid, binds):
    print(f"[{threading.current_thread().name}] Starting EventCheckLoop")
    device = evdev.InputDevice(kbid)

    if "keepDefaultBehaviour" in binds and binds["keepDefaultBehaviour"] == "False":
        device.grab()

    for event in device.read_loop():
        print(f"[{threading.current_thread().name}] T:{event.type}, C:{event.code}, V:{event.value}")
        if (event.type, event.value) in [(evdev.ecodes.EV_KEY, 1)]:
            if f"{event.code}" in binds:
                print(f"[{threading.current_thread().name}] KeyCode {event.code} bound to {binds['%s' % event.code]}")
                RunShell(binds[f"{event.code}"]["run"], binds[f"{event.code}"]["blockThread"])

    if "keepDefaultBehaviour" in binds and binds["keepDefaultBehaviour"] == "False":
        device.ungrab()
