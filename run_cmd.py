#!/usr/bin/env python3
import sys

import subprocess


def run():
    if "--" in sys.argv:
        i = sys.argv.index("--")
        pkg = " ".join(sys.argv[i + 1:])
        args = sys.argv[2:i]
        args.append(pkg)
    else:
        args = [" ".join(sys.argv[2:])]
    args.insert(0, sys.argv[0])
    ret = subprocess.call(args, executable=sys.argv[1])
    exit(ret)


if __name__ == '__main__':
    run()
