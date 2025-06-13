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

import sys
import os
import argparse

from trlc.trlc import Source_Manager
from trlc.errors import Message_Handler

import common

def pp_scope(scope):
    assert isinstance(scope, str)

    scope_map = {
        "All"          : "Up to and including SPARK Platinum",
        "Not_Platinum" : "Up to and including SPARK Gold",
        "Ada"          : "Interfaces and units containing Ada",
        "Automated"    : "N/A - Fully automated",
    }

    if scope in scope_map:
        return scope_map[scope]
    else:
        assert False, "unexpected scope: %s" % data["scope"]


PRIO_TO_NUMBER = {
    "All"    : 0,
    None     : 0,
    "Low"    : 1,
    "Medium" : 2,
    "High"   : 3,
}


def process_checklist_item(fd, obj, min_priority):
    assert min_priority in ("All", "Low", "Medium", "High")

    ok   = True
    data = obj.to_python_dict()

    if not obj.name.startswith("item_"):
        ok = False
        mh.error(obj.loc,
                 "name needs to start with item_",
                 fatal=False)

    if PRIO_TO_NUMBER[data["priority"]] < PRIO_TO_NUMBER[min_priority]:
        return ok

    fd.write(".. rubric:: :cl_%s:`Checklist item %s`" %
             (data["scope"].lower(),
              obj.name[5:].replace("_", ".")))
    if data["automatable"] and data["manual"]:
        fd.write(" (automatable/manual)")
    elif data["automatable"]:
        fd.write(" (automatable)")
    elif data["manual"]:
        fd.write(" (manual)")
    fd.write("\n\n")

    fd.write(".. list-table::\n")
    fd.write("   :widths: 1 3\n")
    fd.write("\n")
    if data["scope"] != "Automated":
        fd.write("   * - Priority\n")
        fd.write("     - %s\n" % data["priority"])
        fd.write("   * - External Review\n")
        fd.write("     - %s\n" % data["ext_review"])

    fd.write("   * - Step\n")
    fd.write("     - %s" % common.fmt_step_link(data["step"]))
    if data["step_to"]:
        fd.write(" .. %s" % common.fmt_step_link(data["step_to"]))
    elif data["step_also"]:
        fd.write(", %s" % common.fmt_step_link(data["step_also"]))
    fd.write("\n")

    fd.write("   * - Scope\n")
    fd.write("     - %s\n\n" % pp_scope(data["scope"]))

    fd.write(data["text"])
    fd.write("\n\n")

    return ok


def process_worklist_item(fd, obj, context):
    ok   = True
    data = obj.to_python_dict()

    if "section" not in context:
        context["section"] = obj.section[-1].name
        context["item"]    = [1, 1]
    elif context["section"] == obj.section[-1].name:
        context["item"][1] += 1
    else:
        context["section"]  = obj.section[-1].name
        context["item"][0] += 1
        context["item"][1]  = 1

    fd.write(".. rubric:: :cl_%s:`Worklist item %u.%u` (%s)\n\n" %
             (data["scope"].lower(),
              context["item"][0],
              context["item"][1],
              context["section"]))

    fd.write("Applies to: %s\n\n" % pp_scope(data["scope"]))

    fd.write(data["text"])
    fd.write("\n\n")

    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("filename")

    ap.add_argument("--min-priority", default="all",
                    help=("emit only checklist items with at least this"
                          "priority ([all]/low/medium/high)"))

    options = ap.parse_args()

    if options.min_priority.lower() not in ("all", "low", "medium", "high"):
        ap.error("minimum priority must be all, low, medium, or high")

    mh = Message_Handler()
    sm = Source_Manager(mh)

    is_worksheet = os.path.basename(options.filename).startswith("ws-")
    if is_worksheet:
        sm.register_file("worksheet.rsl")
    sm.register_file(os.path.join("..", "steps.rsl"))
    sm.register_file("checklist.rsl")
    sm.register_file(options.filename)

    stab = sm.process()

    if stab is None:
        sys.exit(1)

    ok = True
    context = {}
    with open(options.filename.replace(".trlc", ".rst"),
              "w",
              encoding="UTF-8") as fd:
        for obj in stab.iter_record_objects():
            if is_worksheet:
                ok &= process_worklist_item(fd, obj, context)
            else:
                ok &= process_checklist_item(fd, obj,
                                             options.min_priority.capitalize())

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
