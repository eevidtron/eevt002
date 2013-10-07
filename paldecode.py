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
import pylab

# import device drivers
from vxi11Device import Vxi11Device
from usbtmcDevice import UsbtmcDevice
import rigol_ds2000


#####################################################
# read data (from file or scope)

if False:
    print('Reading paldecode.txt..')
    f = open('paldecode.txt', 'r')
    samples = [ float(line) for line in f ]
    f.close()
    timestep = samples[-1]
    samples = samples[0:-1]

else:
    # connect to instrument and download data
    dev = Vxi11Device('192.168.1.20', 'inst0')
    assert dev.ask('trig:stat?').strip() == "STOP"
    dev.write('wav:mode raw')
    dev.write('wav:points %s' % dev.ask(':acq:mdep?').strip())
    samples = rigol_ds2000.download(dev, verbose=True)

    # convert sample bytes to voltages
    yref = float(dev.ask('wav:yref?'))
    yinc = float(dev.ask('wav:yinc?'))
    yori = float(dev.ask('wav:yorigin?'))
    samples = [ (s-yref)*yinc-yori for s in samples ]
    timestep = float(dev.ask('wav:xinc?'))

    # write samples file
    print('Writing paldecode.txt..')
    f = open('paldecode.txt', 'w')
    for s in samples:
        print('%f' % s, file=f)
    print('%g' % timestep, file=f)
    f.close()


#####################################################
# extract one frame

def find_next_sync(samples, start_index):
    while True:
        while True:
            if start_index >= len(samples):
                return (-1, 0)
            if samples[start_index] < -0.15:
                break
            start_index += 1
        stop_index = start_index + 1
        while True:
            if stop_index >= len(samples):
                return (-1, 0)
            if samples[stop_index] > -0.15:
                break
            stop_index += 1
        if (stop_index-start_index) * timestep > 1e-6:
            break
        start_index = stop_index
    if False:
        print('Sync at sample %8d with width %6.2fus.' % (start_index, (stop_index-start_index) * timestep / 1e-6))
    return (stop_index, stop_index-start_index)

index = 0
print('Seeking to 1st line of new frame..')
while True:
    index, width = find_next_sync(samples, index)
    if abs(width * timestep / 1e-6 - 27.3) < 0.5:
        break
while True:
    index, width = find_next_sync(samples, index)
    if abs(width * timestep / 1e-6 - 4.7) < 0.5:
        break

frame = []
for linecount in range(625 // 2):
    print('Decoding line %3d.' % linecount)
    next_index, width = find_next_sync(samples, index)
    index += int(12.05e-6 / timestep)
    cursor = 0
    pixels = []
    for i in range(720):
        pixel = 0
        while cursor < 7.3e-8:
            pixel = max(pixel, samples[index])
            cursor += timestep
            index += 1
        cursor -= 7.3e-8
        pixels.append(pixel)
    if abs(width * timestep / 1e-6 - 4.7) > 0.5:
        break
    index = next_index
    frame.append(pixels)


#####################################################
# plot data

frame = pylab.np.array(frame)
pylab.imshow(frame, cmap='gray')
pylab.show()

