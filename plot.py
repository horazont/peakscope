#!/usr/bin/python3
"""
Copyright 2016 Jonas Schäfer

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
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
