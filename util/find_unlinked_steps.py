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

import os
import re
import difflib


def process(filename, all_steps):
    with open(filename, "r", encoding="UTF-8") as fd:
        content = fd.read()
    lines = [(0, "")]
    for off, c in enumerate(content):
        if c == "\n":
            lines.append((off + 1, ""))
        else:
            lines[-1] = (lines[-1][0], lines[-1][1] + c)

    def get_line(offset):
        line_no = 0
        for line_offset, _ in lines:
            if offset < line_offset:
                return line_no
            line_no += 1
        return line_no

    fixlist = []

    for word in re.finditer("[a-zA-Z_]+", content):
        line_id = get_line(word.span(0)[0])
        line_text = lines[line_id - 1][1]
        if line_text.startswith("Step ID"):
            continue
        if "Steps.ID." in line_text:
            continue

        if word.group(0).lower() in all_steps:
            print("%s:%u: unlinked step %s" % (filename,
                                               line_id,
                                               word.group(0)))
            fixlist.append((word.span(0)[0], word.span(0)[1]))
            continue

        matches = difflib.get_close_matches(word.group(0).lower(),
                                            list(all_steps),
                                            n=1,
                                            cutoff=0.9)

        if matches:
            print("%s:%u: possibly unlinked step %s (did you mean %s?)" %
                  (filename,
                   get_line(word.span(0)[0]),
                   word.group(0),
                   matches[0]))

    for start, end in reversed(fixlist):
        word = content[start:end].lower()
        fixed_word = all_steps[word]
        content = (content[:start] +
                   ":ref:`step-%s`" % word.lower().replace("_", "-") +
                   content[end:])

    with open(filename, "w", encoding="UTF-8") as fd:
        fd.write(content)


def main():
    all_steps = {}
    for path, _, files in os.walk("."):
        for filename in files:
            if filename.endswith(".rst"):
                with open(os.path.join(path, filename),
                          "r",
                          encoding="UTF-8") as fd:
                    for raw_line in fd:
                        if raw_line.startswith("Step ID:"):
                            all_steps[raw_line[8:].strip().lower()] = \
                                raw_line[8:].strip()

    for path, _, files in os.walk("."):
        for filename in files:
            if os.path.splitext(filename)[1] in (".rst",
                                                 ".trlc"):
                process(os.path.join(path, filename), all_steps)


if __name__ == "__main__":
    main()
