#!/usr/bin/python3
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
