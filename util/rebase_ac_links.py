#!/usr/bin/env python3
#
# Ada/SPARK ISO 26262 Process Tools
# Copyright (C) 2024-2025 NVIDIA CORPORATION & AFFILIATES
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

VERSION = "R/docs/gnat-25.1"


def fix_links(match):
    return match.group(1) + VERSION + match.group(3)


def process(file_name):
    with open(file_name, "r", encoding="UTF-8") as fd:
        content = fd.read()

    content = re.sub(
        (r"(https://docs\.adacore\.com/)"
         r"(live/wave|[a-z0-9.]+|R/docs/gnat-[0-9.]+)"
         r"(/[a-zA-Z0-9/_#.]+)"),
        fix_links,
        content)

    with open(file_name, "w", encoding="UTF-8") as fd:
        fd.write(content)


def main():
    for path, _, files in os.walk("."):
        for file_name in files:
            if os.path.splitext(file_name)[1] in (".rst",
                                                  ".csv",
                                                  ".trlc"):
                process(os.path.join(path, file_name))


if __name__ == "__main__":
    main()
