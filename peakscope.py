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
import math
import struct

import numpy


SERIAL_OFFSET = 0x16
SERIAL_LEN = 12
OBSCURE_HEADER_SIZE = 12
HEADER_LEN = 66
CHANNELMAP_OFFSET = 0x35

CH_HEADER_LEN = 0x3b
CH_TIMESCALE_OFFSET = 0x1b
CH_VOLTSCALE_OFFSET = 0x23
CH_YSHIFT_OFFSET = 0x1f
CH_DATA_OFFSET = 0x3b
CH_TYPE_OFFSET = 0x0b


def _count_high_bits(n):
    count = 0
    while n > 0:
        if n & 1:
            count += 1
        n = n >> 1
    return count


class ChannelData:
    def __init__(self, buf=None):
        super().__init__()
        self._data = None
        self._name = None
        self._timescale = None
        self._voltscale = None
        self._yshift = None

        if buf is not None:
            self.decode_from_buf(buf)

    def decode_from_buf(self, buf):
        self._data = numpy.frombuffer(
            buf[CH_DATA_OFFSET:],
            dtype=numpy.int16) / 128 * 5
        self._name = buf[:3].decode("ascii")
        self._timescale = num_to_timescale(buf[CH_TIMESCALE_OFFSET])
        self._voltscale = num_to_voltscale(buf[CH_VOLTSCALE_OFFSET])
        self._yshift = struct.unpack(
            "<l",
            buf[CH_YSHIFT_OFFSET:CH_YSHIFT_OFFSET+4]
        )[0]

    @property
    def data(self):
        return self._data

    @property
    def name(self):
        return self._name

    @property
    def timescale(self):
        return self._timescale

    @property
    def voltscale(self):
        return self._voltscale

    @property
    def yshift(self):
        return self._yshift

    def __repr__(self):
        return ("<{}.{} {!r} {}ns/div {}mV/div "
                "yshift={:+.2f}div #samples={}>").format(
                    type(self).__module__,
                    type(self).__qualname__,
                    self._name,
                    self._timescale,
                    self._voltscale,
                    self._yshift,
                    len(self._data)
                )


class Bin:
    def __init__(self, buf=None):
        super().__init__()
        self._channels = []
        self._serial = None
        self._tshift = None

        if buf is not None:
            self.decode_from_buf(buf)

    def decode_from_buf(self, buf):
        if len(buf) < 66:
            raise ValueError("buffer too small, cannot contain full header")

        self._channels.clear()
        self._serial = buf[SERIAL_OFFSET:SERIAL_OFFSET+SERIAL_LEN]

        payload_sz = struct.unpack("<h", buf[:2])[0]

        channelmap = buf[CHANNELMAP_OFFSET]
        num_channels = _count_high_bits(channelmap)

        channel_data_sz = (
            payload_sz + OBSCURE_HEADER_SIZE - HEADER_LEN
        ) / num_channels
        assert channel_data_sz == int(channel_data_sz)
        channel_data_sz = int(channel_data_sz)

        offset = HEADER_LEN
        for ch in range(num_channels):
            self._channels.append(
                ChannelData(buf[offset:offset+channel_data_sz])
            )
            offset += channel_data_sz

    @property
    def channels(self):
        return self._channels

    def __repr__(self):
        return "<{}.{} #chs={} serial={!r}>".format(
            type(self).__module__,
            type(self).__qualname__,
            len(self._channels),
            self._serial
        )


def num_to_timescale(num):
    exp = math.floor(num/3)
    mant = {0: 1, 1: 2, 2: 5}[num % 3]
    return mant * 10**exp


def num_to_voltscale(num):
    num += 4
    exp = math.floor(num/3)
    mant = {0: 1, 1: 2, 2: 5}[num % 3]
    return mant * 10**exp


def dump_channel_meta(data):
    print(data[:3].decode())
    print(" time scale: {} ns/div".format(num_to_timescale(data[0x1b])))
    print(" volt scale: {} mV/div".format(num_to_voltscale(data[0x23])))
    print(" yshift: {} div".format(
        struct.unpack("<l", data[0x1f:0x1f+4])[0]*0.04
    ))
    # data = numpy.frombuffer(data[0x3b:], numpy.int16)


def dump_meta(data):
    payload_sz, = struct.unpack("<h", data[:2])
    print("size of payload: {}".format(payload_sz))
    print("header size: {}".format(len(data)-payload_sz))
    print("channel map: {:02b}".format(data[0x35]))

    num_channels = 2 if data[0x35] == 3 else 1

    channel_data_sz = (payload_sz + 12 - 0x42) / num_channels
    assert channel_data_sz == int(channel_data_sz)
    channel_data_sz = int(channel_data_sz)

    dump_channel_meta(data[0x42:0x42+channel_data_sz])

    if data[0x35] == 3:
        dump_channel_meta(data[0x42+channel_data_sz:0x42+channel_data_sz*2])
