#!/usr/bin/python3
import mmap

import peakscope


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="+",
    )

    args = parser.parse_args()

    for filename in args.files:
        print(filename)
        with open(filename, "rb") as f:
            scopebin = peakscope.Bin(
                mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
            )
            print(" ", scopebin)
            for ch in scopebin.channels:
                print(" ", ch)
