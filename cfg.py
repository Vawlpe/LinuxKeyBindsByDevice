import json
import os.path
import threading
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

# TODO: WriteCfg func
# TODO: CfgWizard func
