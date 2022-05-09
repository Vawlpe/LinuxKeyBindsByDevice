import json
import os.path
import threading

import evdev

import kbeIntercepter


def ReadCfg(path):
    print(f"[cfg.ReadCfg] Loading from {path}")
    data = json.load(open(os.path.expanduser(path)))
    threads = []
    for kbID, binds in data.items():
        print(f"[cfg.ReadCfg] Creating thread for {kbID}")
        threads.append(threading.Thread(
            target=kbeIntercepter.EventCheckLoop,
            args=(kbID, binds,)
        ))

    for t in threads:
        print(f"[cfg.ReadCfg] Starting thread {t.name}")
        t.start()


def WriteCfg(data, path):
    json.dump(data, open(os.path.abspath(path)))


def CfgWizard():
    print("[CfgWizard] Starting config generation wizard")
    print("[CfgWizard] Scanning for input devices...")
    devices = [path for path in os.listdir("/dev/input/by-id")]
    WizardAddDevice(devices)


def WizardAddDevice(devices):
    print("[CfgWizard] Found devices:")
    for i in range(len(devices)):
        print(f"\t{i}: {devices[i]}")

    di = input(f"[CfgWizard] Choose a device to configure [0-{len(devices) - 1}], or exit (Q)): ")
    if di.lower() == "q":
        return

    d = devices[int(di)]

    WizardAddKeybind()

def WizardAddKeybind(binds):
    if len(binds) > 0:
        print("Existing keybinds:")
        for b in binds:
            print(b)
    else:
        binds = {}

    kcode = input("Keycode or exit (Q): ")
    if kcode.lower() == "q":
        return binds

    rcmd = input("Command to run or exit (Q): ")
    if rcmd.lower() == "q":
        return binds

    tblck = input("Should this command block the device read loop thread? (y/N)").lower() in ["yes", "y"]

    #TODO: fix whatever this is
    binds.append(kcode,
        {
            "run": rcmd,
            "blockThread": tblck
        }
    })
