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
import sys

def data2array(data):
    assert data[0] == '#'
    samplenum = int(data[2:int(data[1])+2])
    return bytearray(data[int(data[1])+2:int(data[1])+2+samplenum])

def download(dev, verbose=False):
    dev.write('wav:reset')
    dev.write('wav:begin')
    data = []
    if verbose:
        print('Downloading data from scope...', file=sys.stderr)
    while True:
        status = dev.ask('wav:stat?').strip()
        block = data2array(dev.ask('wav:data?'))
        if verbose:
            print('  downloaded block with %6d bytes, total=%8d, status=%s' % (len(block), len(data), status), file=sys.stderr)
        data.extend(block)
        if status[0] == 'I':
            break
    dev.write('wav:end')
    return data

