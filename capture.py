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
import socket
import struct


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=3000,
    )
    parser.add_argument(
        "--host",
        default="192.168.1.72",
        nargs="?"
    )
    parser.add_argument(
        "outfile",
    )

    args = parser.parse_args()

    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )
    s.connect((args.host, args.port))
    s.send(b"STARTBIN")
    s.setblocking(True)
    with open(args.outfile, "wb") as f:
        szbuf = s.recv(2)
        assert len(szbuf) == 2
        sz = 12+struct.unpack("<H", szbuf)[0]
        f.write(szbuf)

        read = 2
        read_total = 2
        recvbuf = bytearray(1024)
        while read_total < sz:
            read = s.recv_into(recvbuf, 1024)
            read_total += read
            f.write(recvbuf[:read])
    s.close()
