import json
import os.path
import threading
import kbeIntercepter


def ReadCfg(path):
    print(f"[ReadCfg] Loading from {path}")
    data = json.load(open(os.path.expanduser(path)))
    threads = []
    for kbID, binds in data.items():
        print(f"[ReadCfg] Creating thread for {kbID}")
        threads.append(threading.Thread(
            target=kbeIntercepter.EventCheckLoop,
            args=(kbID, binds,)
        ))

    for t in threads:
        print(f"[ReadCfg] Starting thread {t.name}")
        t.start()


def WriteCfg(data, path):
    json.dump(data, open(os.path.abspath(path)))


def CfgWizard():
    print("[CfgWizard] Starting config generation wizard")
    print("[CfgWizard] Scanning for input devices...")
    devices = [path for path in os.listdir("/dev/input/by-id")]
    bindings = WizardAddDevice(devices)
    if len(bindings) > 0:
        print(f"\n----------------------------\n{bindings}\n----------------------------")
        if input("[CfgWizard] Finishing up configuration, are you sure you want to keep this configuration? (y/N): ").lower() in ["yes", "y"]:
            WriteCfg(bindings, os.path.expanduser('~/.config/lkbbd.json'))
            input("[CfgWizard] Done, re-run lkbbd and it should detect the new configuration")
        else:
            print("[CfgWizard] DISCARDING CONFIG AND EXITING...")
            return


def WizardAddDevice(devices, bindings={}):
    print("[CfgWizard] Found devices:")
    for i in range(len(devices)):
        print(f"\t{i}: {devices[i]}")

    di = input(f"[CfgWizard] Choose a device to configure [0-{len(devices) - 1}], or exit (Q)): ")
    if di.lower() == "q":
        return

    d = devices[int(di)]

    binds = WizardAddKeybind()
    if len(binds) > 0:
        print(f"[CfgWizard] Device {di}: ({devices[int(di)]}) configured with the following bindings: ")
        for k, b in binds.items():
            print(f"\t{k} -> {b['run']}{' (blocking)' if b['blockThread'] == 'True' else ''}")

        fwd = input(f"[CfgWizard] Do you wish to allow the default actions of keybinds for this device to still trigger? (y/N): ").lower() in ["yes", "y"]

        binds.update({"keepDefaultBehaviour": f"{fwd}"})
        bindings.update({os.path.join("/dev/input/by-id/", devices[int(di)]): binds})

        if input(f"[CfgWizard] Bindings for device {di} have been configured, do you wish to configure another device? (y/N): ").lower() in ["yes", "y"]:
            return WizardAddKeybind(devices, bindings)
    else:
        if input(f"[CfgWizard] There were no valid bindings configured for device {di}, do you wish to configure another device? (y/N): ").lower() in ["yes", "y"]:
            return WizardAddKeybind(devices, bindings)

    return bindings


def WizardAddKeybind(binds={}):
    if len(binds) > 0:
        print("[CfgWizard] Existing keybinds:")
        for b in binds:
            print(f"\t{b}")

    kcode = input("[CfgWizard] Keycode or exit (Q): ")
    if kcode.lower() == "q":
        return binds

    rcmd = input("[CfgWizard] Command to run or exit (Q): ")
    if rcmd.lower() == "q":
        return binds

    tblck = input("[CfgWizard] Should this keybind block the device read loop thread? (y/N)").lower() in ["yes", "y"]

    binds.update({
        f"{kcode}": {
            "run": rcmd,
            "blockThread": f"{tblck}"
        }
    })

    print(f"[CfgWizard] Added Keybind for {kcode} -> {rcmd}{' (blocking)' if tblck else ''}")

    if input("[CfgWizard] Do you want to add another keybind? (y/N): ").lower() in ["yes", "y"]:
        return WizardAddKeybind(binds)

    return binds


