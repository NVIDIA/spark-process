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

import textwrap
import csv
import os
import re

from trlc.errors import Message_Handler
from trlc.trlc import Source_Manager


def mk_context(filename):
    base = os.path.splitext(os.path.basename(filename))[0]
    context = {
        "tool"            : None,
        "status"          : None,
        "is_switch"       : True,
        "warning_related" : False,
    }
    if base.startswith("compiler_"):
        context["tool"]            = "GNAT_Compiler"
        context["warning_related"] = "warning_" in base
    elif base.startswith("gnatcheck_"):
        context["tool"] = "GNAT_Check"
    elif base.startswith("gnatprove_"):
        context["tool"] = "SPARK"
    else:
        assert False
    if base.endswith("_required"):
        context["status"] = "Required"
    elif base.endswith("_required_rules"):
        context["status"] = "Required"
        context["is_switch"] = False
    elif base.endswith("_optional"):
        context["status"] = "Allowed"
    elif base.endswith("_banned"):
        context["status"] = "Banned"
    else:
        assert False

    return context


uid_counters = {
    "GNAT_Compiler" : 0,
    "GNAT_Check"    : 0,
    "SPARK"         : 0,
}


def fmt_switches(context, mixed_switches, justification, steps):
    switches = []
    for mixed_switch in mixed_switches.splitlines():
        try:
            switch, switch_note = mixed_switch.split(" ", 1)
        except ValueError:
            switch      = mixed_switch
            switch_note = None
        switches.append((switch, switch_note))

    rv = []

    if context["tool"] == "GNAT_Compiler":
        uid = "Compiler_"
    elif context["tool"] == "GNAT_Check":
        uid = "Check_"
    elif context["tool"] == "SPARK":
        uid = "SPARK_"
    else:
        assert False
    if context["is_switch"]:
        uid += "Switch_"
    else:
        uid += "Rule_"
    if len(switches) == 1:
        if context["is_switch"]:
            uid += switches[0][0].lstrip("-_").split("=", 1)[0]
        else:
            uid += switches[0][0].lstrip("-_")
            uid = uid.replace("=>", "_")
        if "gnatw" in uid:
            head, tail = uid.split("gnatw", 1)
            if tail.lstrip("._")[0] == tail.lstrip("._")[0].lower():
                uid = head + "Warning_Lowercase"
            else:
                uid = head + "Warning_Uppercase"
            uid += tail.replace("_", "_Underscore_")
        uid = uid.replace("-", "_")
        uid = uid.replace(":", "_")
        uid = uid.replace("+", "Plus_")
        uid = uid.replace("-", "Minus_")
        uid = uid.replace("<", "")
        uid = uid.replace(">", "")
        uid = uid.replace(".", "_Dot_")
        if uid == "SPARK_Switch_u":
            uid = "SPARK_Switch_Lowercase_U"
        elif uid == "SPARK_Switch_U":
            uid = "SPARK_Switch_Uppercase_U"
        elif uid == "SPARK_Switch_prover" and context["status"] == "Banned":
            uid = "SPARK_Switch_Banned_Provers"

    else:
        uid_counters[context["tool"]] += 1
        uid += "Group_%u" % uid_counters[context["tool"]]

    if context["tool"] == "GNAT_Compiler":
        rv.append("Compiler_Switch_Constraint %s {" % uid)
    elif not context["is_switch"]:
        rv.append("Rule_Constraint %s {" % uid)
    else:
        rv.append("Switch_Constraint %s {" % uid)

    if not context["is_switch"]:
        pass
    elif context["tool"] != "GNAT_Compiler":
        rv.append("   tool         = Tool.%s" % context["tool"])
    else:
        rv.append("   warn_related = %s" %
                  str(context["warning_related"]).lower())
    rv.append("   status       = Status.%s" % context["status"])

    if context["is_switch"]:
        rv.append("   switches     = [")
        first = True
        for switch, note in switches:
            if first:
                first = False
            else:
                rv[-1] += ","
            if note:
                rv.append("     // %s"  % note)
            rv.append("     Pattern.Prefix: \"%s\"" % switch)
        rv.append("   ]")
    else:
        assert len(switches) == 1
        switch, note = switches[0]
        if note:
            rv.append("   // %s"  % note)
        rv.append("   rule = \"%s\"" % switch)

    rv.append("   rationale    = '''")
    justification = re.sub(r"(-gn[a-z0-9_.]*[a-z0-9])",
                           r"``\1``",
                           justification)
    tmp = []
    for word in justification.split():
        if word.lower() in steps:
            tmp.append(":ref:`%s <step-%s>`" %
                       (word,
                        word.lower().replace("_", "-")))
        else:
            tmp.append(word)

    justification = " ".join(tmp)

    rv += textwrap.wrap(justification,
                        initial_indent    = " " * 5,
                        subsequent_indent = " " * 5,
                        break_on_hyphens  = False)
    rv.append("   '''")

    rv.append("}")

    return rv


def process(filename, steps):
    context = mk_context(filename)
    row_id = 0
    with open(filename, "r", encoding="UTF-8") as fd_in:
        for switches, justification in csv.reader(fd_in):
            row_id += 1
            rv = fmt_switches(context, switches, justification, steps)
            print()
            print("// from %s, row %u" % (os.path.basename(filename), row_id))
            print("\n".join(rv))


def main():
    sm = Source_Manager(Message_Handler())
    sm.register_file("../steps.rsl")
    ast = sm.process()
    pkg_steps = ast.lookup_assuming(sm.mh, "Steps")
    enum_steps = pkg_steps.symbols.lookup_assuming(sm.mh, "ID")
    steps = [lit.lower()
             for lit in enum_steps.literals.all_names()
             if lit.upper() != lit]

    print("package Switches")
    for f in sorted(os.listdir("..")):
        if f.endswith(".csv"):
            process(os.path.join("..", f), steps)


if __name__ == "__main__":
    main()
