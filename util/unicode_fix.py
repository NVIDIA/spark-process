#!/usr/bin/env python3
#
# Ada/SPARK ISO 26262 Process Tools
# Copyright (C) 2024 NVIDIA CORPORATION & AFFILIATES
#
# This file is part of the NVIDIA SPARK ISO 26262 Process.
#
# The NVIDIA SPARK ISO 26262 Process Tools are free software: you can
# redistribute them and/or modify them under the terms of the GNU
# General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later
# version.
#
# The NVIDIA SPARK ISO 26262 Process Tools are distributed in the hope
# that they will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the NVIDIA SPARK ISO 26262 Process Tools. If not, see
# <https://www.gnu.org/licenses/>.

import argparse
import csv
import os
import sys


REPL = {
    "’" : "'",
    "‘" : "'",
    "“" : "\"",
    "”" : "\"",
    "…" : "...",
    "–" : "-",
    "—" : "-",
    "‑" : "-",
    "‐" : "-",
    "®" : " (R)",
    "™" : " (TM)",
    "•" : "*",
}


def process(file_name, content):
    complaints = set()
    tmp = ""

    for c in content:
        if c.isascii():
            pass

        elif c in "Ü":
            pass

        elif c == "\ufeff":
            continue

        elif c == "\u200b":
            # zero width space
            continue

        elif c in REPL:
            c = REPL[c]

        elif c not in complaints:
            complaints.add(c)
            print("unprintable", repr(c), ord(c), c)
            c = ""

        tmp += c

    if complaints:
        print("please fix %s or script to deal with the problems" % file_name)
        sys.exit(1)

    return tmp


def main():
    ap = argparse.ArgumentParser(description="sanitise non-ascii characters")

    ap.add_argument("-o",
                    metavar="FILENAME",
                    help="output filename, otherwise overwrite input file")
    ap.add_argument("input_file")
    ap.add_argument("--csv",
                    action="store_true",
                    default=False,
                    help="treat input as a csv file")

    options = ap.parse_args()

    if not os.path.isfile(options.input_file):
        ap.error("%s is not a file" % options.input_file)

    if options.o and \
       os.path.exists(options.o) and \
       not os.path.isfile(options.o):
        ap.error("output file %s already exists and is not a file" %
                 options.o)

    with open(options.input_file, "r", encoding="UTF-8") as fd:
        if options.csv:
            reader = csv.reader(fd)
            content = list(reader)
        else:
            content = fd.read()

    if options.csv:
        content = [[process(options.input_file, item) for item in row]
                   for row in content]
    else:
        content = process(options.input_file, content)

    with open(options.o if options.o else options.input_file,
              "w",
              encoding="UTF-8") as fd:
        if options.csv:
            writer = csv.writer(fd, lineterminator="\n")
            for row in content:
                writer.writerow(row)
        else:
            fd.write(content)


if __name__ == "__main__":
    main()
