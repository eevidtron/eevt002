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
#
# this program is part of a response to the following comment on reddit:
# http://www.reddit.com/r/eevidtron/comments/1o5f8h/eevt002_controlling_measurement_equipment_with/ce80mgn

# boilerplate code
from __future__ import division
from __future__ import print_function
import time

# import UsbtmcDevice
from usbtmcDevice import UsbtmcDevice

# connect to instrument
dev = UsbtmcDevice('/dev/usbtmc0')

# execute a single step of the sequence
def seq_step(freq, volt, off, phase, secs):
    dev.write('func sin')
    dev.write('freq %f' % freq)
    dev.write('volt %f' % volt)
    dev.write('volt:offs %f' % off)
    dev.write('phas %f' % phase)
    time.sleep(0.5)
    dev.write('output on')
    time.sleep(secs)
    dev.write('output off')
    time.sleep(0.5)

# reset
dev.write('*rst')
time.sleep(1.0)

# sequence
seq_step(  100, 10, 5, 180, 8 * 60)
seq_step(12548, 12, 2, 180, 4 * 60)
seq_step( 5000,  8, 4,  90, 3 * 60)

