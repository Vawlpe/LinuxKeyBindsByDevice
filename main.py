#!/bin/python

import sys
import cfg
import os.path as path


def main(args):
    print(f"[main.main] Args: {args}")
    if len(args) < 2:
        execPath = path.abspath(path.dirname(args[0]))
        print(f"Looking for config @ {path.expanduser('~/.config.lkbbd.json')}")
        if path.exists(path.expanduser("~/.config/lkbbd.json")):
            cfg.ReadCfg("~/.config/lkbbd.json")
            return

        print(f"Looking for config @ {path.join(execPath, 'lkbbd.json')}")
        if path.exists(path.join(execPath, "lkbbd.json")):
            cfg.ReadCfg(path.join(execPath, "lkbbd.json"))
            return

        # TODO: fix this shit
        # if not extraPathCheck():
        #     inp = input(f"Do you want to generate a new config @ {path.expanduser('~/.config/lkbbd.json')} (y/N): ")
        #     if inp.lower() in ["yes", "y"]:
        #         cfg.CfgWizard()
        #     else:
        #         print("Exiting, no config possible")
        #         return
    else:
        cfg.ReadCfg(args[1])


def extraPathCheck():
    inp = input("No config found, do you want to try a different path? (y/N): ")
    if inp.lower() in ["yes", "y"]:
        p = input("Input a custom config file path: ")
        if path.exists(path.abspath(p)):
            cfg.ReadCfg(path.abspath(p))
            return True
        else:
            return extraPathCheck()
    else:
        return False


if __name__ == '__main__':
    main(sys.argv)

