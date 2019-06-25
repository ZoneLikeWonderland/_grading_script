#!/usr/bin/env python3
import sys

from run_cmd import run

if __name__ == '__main__':
    package = False
    for arg in sys.argv:
        if arg == '--':
            package = True
            continue
        if package:
            if '/' in arg:
                exit(1)
    run()
