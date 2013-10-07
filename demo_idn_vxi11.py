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

# import PyVXI11
from vxi11Device import Vxi11Device

# connect to instrument
dev = Vxi11Device('192.168.1.20', 'inst0')

# query and output identification string
answer = dev.ask('*IDN?').strip()
print(answer)

