#!/bin/python

import sys
import cfg


def main(args):
    print(f"[main.main] Args: {args}")
    if len(args) < 1:
        # TODO: if no args, or config doesn't exist, bring up cfg.CfgWizard
        cfg.ReadCfg("~/.config/lkbbd.json")
    else:
        cfg.ReadCfg(args[0])


if __name__ == '__main__':
    main(sys.argv[1:])

