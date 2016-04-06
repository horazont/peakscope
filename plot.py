#!/usr/bin/python3
import sys

import numpy as np

import matplotlib.pyplot as pyplot

import peakscope


scopebin = peakscope.Bin(open(sys.argv[1], "rb").read())

chlines = []
for ch in scopebin.channels:
    full_ts = 15*ch.timescale * 1e-9
    ts = np.linspace(-full_ts/2, full_ts/2, len(ch.data))
    chlines.append((
        pyplot.plot(ts, ch.data * ch.voltscale * 1e-3)[0],
        ch.name
    ))


pyplot.figlegend([line for line, *_ in chlines],
                 [name for _, name, *_ in chlines],
                 'upper right')


pyplot.xlabel("time [s]")
pyplot.ylabel("voltage [V]")
pyplot.show()
