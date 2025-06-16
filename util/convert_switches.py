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

import csv
import glob
import textwrap

constraint_id = {
    "GNAT_Compiler" : 0,
    "GNAT_Check"    : 0,
    "SPARK"         : 0,
}


def process(fd, row, tool, status, is_warning_related, is_rule):
    fields = {
        "tool"      : "Tool.%s" % tool,
        "status"    : "Status.%s" % status,
        "rationale" : row[1]
    }

    if is_rule:
        assert tool == "GNAT_Check"
        rec_type      = "Rule_Constraint"
        fields["rule"] = row[0]
    else:
        if tool == "GNAT_Compiler":
            rec_type               = "Compiler_Switch_Constraint"
            fields["warn_related"] = str(is_warning_related).lower()
        else:
            rec_type = "Switch_Constraint"

        fields["switches"] = ['Pattern.Verbatim : "%s"' % switch
                              for switch in row[0].split()]

    constraint_id[tool] += 1
    fd.write("%s %s_constraint_%u {\n" % (rec_type,
                                          tool.lower(),
                                          constraint_id[tool]))
    if rec_type == "Switch_Constraint":
        fd.write("  tool = %s\n" % fields["tool"])
    if rec_type == "Compiler_Switch_Constraint":
        fd.write("  warn_related = %s\n" % fields["warn_related"])
    fd.write("  status = %s\n" % fields["status"])
    fd.write("\n")

    if rec_type == "Rule_Constraint":
        fd.write("  rule = \"%s\"" % fields["rule"])
    else:
        fd.write("  switches = [")
        for i, switch_spec in enumerate(fields["switches"]):
            if i > 0:
                fd.write(",\n")
                fd.write("              ")
            fd.write(switch_spec)
        fd.write("]\n")

    fd.write("\n")
    fd.write("  rationale = '''\n")
    for line in fields["rationale"].splitlines():
        if len(line) > 70:
            for sub_line in textwrap.wrap(line):
                fd.write("    %s\n" % sub_line.rstrip())
        else:
            fd.write("    %s\n" % line.rstrip())
    fd.write("  '''\n")
    fd.write("}\n\n")


def main():
    # pylint: disable=consider-using-with
    out_file = {
        "GNAT_Compiler" : open("switches/compiler.trlc",
                               "w",
                               encoding="UTF-8"),
        "GNAT_Check"    : open("switches/gnatcheck.trlc",
                               "w",
                               encoding="UTF-8"),
        "SPARK"         : open("switches/gnatprove.trlc",
                               "w",
                               encoding="UTF-8"),
    }

    for fd in out_file.values():
        fd.write("package Switches\n\n")

    for file_name in sorted(glob.glob("*.csv")):
        tool = None
        warn = None
        stat = None
        rule = False

        if file_name.startswith("compiler_warning_"):
            tool = "GNAT_Compiler"
            warn = True
        elif file_name.startswith("compiler_"):
            tool = "GNAT_Compiler"
            warn = False
        elif file_name.startswith("gnatprove_"):
            tool = "SPARK"
        else:
            assert file_name.startswith("gnatcheck_")
            tool = "GNAT_Check"
            rule = "_rules" in file_name

        if "required" in file_name:
            stat = "Required"
        elif "optional" in file_name:
            stat = "Allowed"
        else:
            assert "banned" in file_name
            stat = "Banned"

        with open(file_name, "r", encoding="UTF-8") as fd:
            for row in csv.reader(fd):
                process(out_file[tool], row, tool, stat, warn, rule)


if __name__ == "__main__":
    main()
