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
import time
import pylab

# import device drivers
from vxi11Device import Vxi11Device
from usbtmcDevice import UsbtmcDevice
import rigol_ds2000

# list of all builtin waveforms (copied from RIGOL DG1000 Programming Guide, page 2-10)
# Note: The "Cardiac" wafeform reads back as "Cardic"; this is a bug in the DG1000 firmware
waveform_names = """
  NegRamp AttALT AmpALT StairDown StairUp StairUD Cpulse PPulse NPulse Trapezia RoundHalf AbsSine AbsSineHalf SINE_TRA SINE_VER
  Exp_Rise Exp_Fall Tan Cot Sqrt X^2 Sinc Gauss HaverSine Lorentz Dirichlet GaussPulse Airy
  Cardiac Quake Gamma Voice TV Combin BandLimited Stepresponse Butterworth Chebyshev1 Chebyshev2
  Boxcar Barlett triang Blackman Hamming Hanning Kaiser
  Roundpm
""".upper().split()

# connect to instruments
dev_fgen = UsbtmcDevice('/dev/usbtmc_fgen')
dev_scope = Vxi11Device('192.168.1.20', 'inst0')

print('Resetting devices..')
dev_scope.write('*rst')
dev_fgen.write('*rst')
time.sleep(2.0)

print('Setting up devices..')
dev_scope.write('chan1:disp on')
dev_scope.write('chan1:probe 1')
dev_scope.write('chan1:scale 1')
dev_scope.write('chan1:offset 1')

dev_scope.write('chan2:disp on')
dev_scope.write('chan2:probe 1')
dev_scope.write('chan2:scale 5')
dev_scope.write('chan2:offset -15')

dev_scope.write('timebase:offset 5e-4')
dev_scope.write('timebase:scale 1e-4')

dev_scope.write('trig:mode edge')
dev_scope.write('trig:edge:source chan2')
dev_scope.write('trig:edge:slope pos')
dev_scope.write('trig:edge:level 2.5')

dev_fgen.write('output on')
dev_fgen.write('output:sync on')
time.sleep(2.0)

# initialize and show figure
pylab.figure()
pylab.show(block = False)

# for all built-in waveforms
for wf in waveform_names:

    # set function generator to waveform
    dev_fgen.write('func:user %s' % wf)
    wf_readback = dev_fgen.ask('func:user?').strip()

    # wait a second and sample waveform using scope
    time.sleep(1.0)
    samples = rigol_ds2000.data2array(dev_scope.ask('wav:data?'))

    # convert sample bytes to voltages
    yref = float(dev_scope.ask('wav:yref?'))
    yinc = float(dev_scope.ask('wav:yinc?'))
    yori = float(dev_scope.ask('wav:yorigin?'))
    samples = [ (s-yref)*yinc-yori for s in samples ]

    # plot data and create png files
    pylab.clf()
    pylab.plot(samples[200:1200])
    if wf == wf_readback:
        pylab.title('%s' % wf)
    else:
        pylab.title('%s (%s)' % (wf, wf_readback))
    pylab.draw()
    pylab.savefig('dg1000_%s.png' % wf.lower())
    print('written dg1000_%s.png.' % wf.lower())

# create html file
f = open('dg1000_builtins.html', 'w')
for wf in waveform_names:
    print('<img src="dg1000_%s.png"/><br/>' % wf.lower(), file=f)
f.close()
print('written dg1000.html.')

