#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261120.

Writes the front-page image to /output/entry.png.

The image is drawn by draw.py (same repository) from the verified news
of Friday 20 November 2026; this program only copies that file, so both
grading runs produce byte-identical output. Standard library only, no
network, no fonts needed at run time.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print("wrote", dst)


if __name__ == "__main__":
    sys.exit(main())
