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
import sys
import re
import argparse

from pprint import pprint

MARKER_ALL = "when using SPARK on all or part of a program"
MARKER_PART = "when using SPARK on only part of a program"
MARKER_MODULAR = ("the complete SPARK program is analyzed"
                  " by calling GNATprove multiple times")
MARKER_COMPILER = "when compiling the program with another compiler"


def process(fd, lines):
    assumptions = []
    assumption_body = None
    assumption_name = None
    assumption_kind = None
    skip_until = None

    fd.write("package Gnatprove_Assumptions\n\n")

    def emit_assumption():
        assert assumption_kind is not None
        while not assumption_body[-1].strip():
            del assumption_body[-1]

        text_body = ""
        for line in assumption_body:
            text_body += "    " + line.rstrip() + "\n"

        # TODO: Replace with links to the SPARK UG, if possible
        text_body = re.sub(r":ref:`(.*?)`",
                           r"\1",
                           text_body,
                           flags=re.DOTALL)

        text_body = re.sub(r"\[(.*?)\]",
                           r"[[\1]]",
                           text_body,
                           flags=re.DOTALL)

        text_body = re.sub(r"\|(.*?)\|",
                           r"\1",
                           text_body,
                           flags=re.DOTALL)

        fd.write("Gnatprove_Assumption %s {\n" % assumption_name)
        fd.write("  kind = Kind.%s\n" % assumption_kind.capitalize())
        fd.write("  text = '''\n")
        for line in text_body.splitlines():
            fd.write(line.rstrip() + "\n")
        fd.write("  '''\n")
        fd.write("}\n\n")

    for line_no, line in enumerate(lines):
        if skip_until is not None and line_no < skip_until:
            continue
        else:
            skip_until = None

        if line.startswith("* "):
            if assumption_name is not None:
                emit_assumption()
            assumption_name = re.match(r"\* \[(.*)\]", line).group(1)
            assumption_body = []

        elif not line.startswith("  ") and len(line.strip()):
            if assumption_name is not None:
                emit_assumption()
                assumption_name = None
                assumption_body = []
            full_par = ""
            while line_no < len(lines) and \
                  not (lines[line_no].startswith(" ") or
                       lines[line_no].startswith("*")):
                if not lines[line_no].strip():
                    break
                full_par = (full_par + " " + lines[line_no]).strip()
                line_no += 1
                skip_until = line_no

            if full_par.startswith(".. index"):
                continue

            if MARKER_ALL in full_par:
                assumption_kind = "all"
            elif MARKER_PART in full_par:
                assumption_kind = "part"
            elif MARKER_MODULAR in full_par:
                assumption_kind = "modular"
            elif MARKER_COMPILER in full_par:
                assumption_kind = "compiler"
            else:
                assumption_kind = None

        elif assumption_name is not None:
            if line.startswith("  "):
                assumption_body.append(line[2:])
            else:
                assumption_body.append(line)

    if assumption_name is not None:
        emit_assumption()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spark_repo",
                    help = "root path to a spark 2014 checkout")
    options = ap.parse_args()

    if not os.path.isdir(options.spark_repo):
        ap.error("%s not a directory" % options.spark_repo)

    assumption_file = os.path.join(options.spark_repo,
                                   "docs", "ug", "en", "source",
                                   "how_to_use_gnatprove_in_a_team.rst")

    if not os.path.isfile(assumption_file):
        ap.error("cannot open %s" % assumption_file)

    du_cfg = {
        "report_level": 4,
    }

    in_relevant_section = False
    relevant_lines = []
    with open(assumption_file, "r", encoding="UTF-8") as fd:
        for raw_line in fd:
            if raw_line.startswith("Complete List of Assumptions"):
                in_relevant_section = True
            if in_relevant_section:
                relevant_lines.append(raw_line.rstrip())

    with open(os.path.join("source",
                           "process",
                           "tracing",
                           "spark_assumptions",
                           "spark-assumptions.trlc"),
              "w", encoding="UTF-8") as fd:
        fd.write("// generated from %s, do not edit by hand\n\n" %
                 os.path.basename(assumption_file))
        process(fd, relevant_lines)


if __name__ == "__main__":
    main()
