#!/usr/bin/python
#
# eevidtron example code (youtube.com/eevidtron)
# written by Clifford Wolf (www.clifford.at)
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.

# boilerplate code
from __future__ import division
from __future__ import print_function

# used standard libraries
import os
import time

class UsbtmcDevice:
    """
    Simple usbmtc device abstraction with a minimal VISA-like API
    """

    def __init__(self, device="/dev/usbtmc0"):
        self.f = os.open(device, os.O_RDWR)

    def __del__(self):
        os.close(self.f)

    def write(self, cmd):
        os.write(self.f, cmd)
        time.sleep(0.01)

    def read(self):
        return os.read(self.f, 4096)

    def ask(self, cmd):
        self.write(cmd)
        return self.read()

