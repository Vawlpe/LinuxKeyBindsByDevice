import os
import struct
import threading


def RunShell(cmd):
    os.system(f"{cmd} &")

# TODO: Intercept default key behaviour

def EventCheckLoop(kbid, binds):
    print(f"[{threading.current_thread().name}] Opening device file @ {kbid}")
    FORMAT = 'llHHI'
    EVENT_SIZE = struct.calcsize(FORMAT)
    kb = open(kbid, "rb")
    event = kb.read(EVENT_SIZE)

    print(f"[{threading.current_thread().name}] Starting event loop for {kbid}")
    while event:
        (tv_sec, tv_usec, eventType, code, value) = struct.unpack(FORMAT, event)
        if (eventType, code, value) in [(0, 0, 0)]:
            print(f"[{threading.current_thread().name}] ===========================================")
            pass
        elif (eventType, value) in [(1, 1)]:
            print(f"[{threading.current_thread().name}] KeyDown: {code}")
            if f"{code}" in binds:
                print(f"[{threading.current_thread().name}] KeyCode {code} bound to {binds['%s' % code]}")
                RunShell(binds[f"{code}"])
        else:
            print(f"[{threading.current_thread().name}] T:{eventType}, C:{code}, V:{value}")
            pass
        event = kb.read(EVENT_SIZE)

    kb.close()
