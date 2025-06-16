#!/usr/bin/env python3
#
# Ada/SPARK ISO 26262 Process Tools
# Copyright (C) 2025 NVIDIA CORPORATION & AFFILIATES
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

import re
import sys
import os
import argparse

from trlc.trlc import Source_Manager
from trlc.errors import Location, Message_Handler

import common


def process_checklist_item(mh, fd, refs, loc, name, data):
    assert isinstance(mh, Message_Handler)
    assert isinstance(refs, dict)
    assert isinstance(loc, Location)
    assert isinstance(name, str)
    assert isinstance(data, dict)

    ok = [True]

    def resolve_reference(m):
        step = m.group(1)
        if step.startswith("step-") and step[5:] in refs:
            step = step[5:]
            return ("Step [%s](%s/process/process/%s#%s)" %
                    (common.GH_PAGES_BASE_URL,
                     step.replace("-", " ").capitalize(),
                     refs[step],
                     step))
        else:
            mh.error(loc,
                     "unresolved reference %s in description" % step,
                     fatal=False)
            ok[0] = False

    if not name.startswith("item_"):
        mh.error(loc,
                 "name needs to start with item_",
                 fatal=False)
        return False

    fd.write("\n\n### Checklist item %s (" %
             name[5:].replace("_", "."))
    fd.write(common.pp_scope(data["scope"]))
    if data["priority"]:
        fd.write(", %s Priority" % data["priority"])
    fd.write(")\n\n")

    if data["ext_review"]:
        fd.write("**EXTERNAL REVIEW REQUIRED**\n\n")

    text = data["text"]
    text = re.sub(r":ref:`(.*?)`", resolve_reference, text)
    text = re.sub(r":lrm:`(.*?)`",
                  r"[Ada 2022 LRM (\1)](%s/RM-\1.html)" % common.LRM_BASE_URL,
                  text)
    text = re.sub(r"`(.*?) *<(.*?)>`_", r"[\1](\2)", text)
    text = re.sub(r"``(.*?)``", r"`\1`", text)

    for line in text.splitlines():
        fd.write("> %s\n" % line)

    return ok[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-priority", default="all",
                    help=("emit only checklist items with at least this"
                          "priority ([all]/low/medium/high)"))

    options = ap.parse_args()

    if options.min_priority.lower() not in ("all", "low", "medium", "high"):
        ap.error("minimum priority must be all, low, medium, or high")
    else:
        min_prio = common.PRIO_TO_NUMBER[options.min_priority.capitalize()]

    # Figure out process steps
    steps = {}
    for path, dirs, files in os.walk(os.path.join("..", "process")):
        for file_name in files:
            if not file_name.endswith(".rst"):
                continue
            base_file = os.path.basename(file_name).replace(".rst", ".html")
            with open(os.path.join(path, file_name),
                      "r",
                      encoding="UTF-8") as fd:
                for raw_line in fd:
                    if m := re.match("^Step ID: (.+)$", raw_line.strip()):
                        step_id = m.group(1).lower().replace("_", "-")
                        steps[step_id] = base_file

    # Read checklist sections
    last_line = None
    in_section = None
    sections = []
    with open(os.path.join("..", "checklist.rst"),
              "r",
              encoding="UTF-8") as fd:
        for raw_line in fd:
            line = raw_line.strip()

            if re.match(r"^(\-+)|(\^+)$", line):
                in_section = last_line

            if m := re.match(r"^\.\. include:: checklist/(.+).rst$", line):
                if "ws-" not in m.group(1):
                    sections.append((in_section, m.group(1) + ".trlc"))

            last_line = line

    # Read checklist files
    mh = Message_Handler()
    sm = Source_Manager(mh)
    sm.register_file(os.path.join("..", "steps.rsl"))
    sm.register_file("checklist.rsl")
    for section_name, file_name in sections:
        sm.register_file(file_name)

    stab = sm.process()
    ok   = True

    if stab is None:
        sys.exit(1)

    # Generate checklist
    with open("Checklist_Template_%s.md" % options.min_priority.capitalize(),
              "w", encoding="UTF-8") as fd:
        fd.write("# SPARK Process Checklist (%s)\n" %
                 options.min_priority.upper())

        for section_name, file_name in sections:
            first_item = True
            for obj in stab.iter_record_objects():
                if obj.location.file_name != file_name:
                    continue

                # Filter out low-prio items
                data = obj.to_python_dict()
                if common.PRIO_TO_NUMBER[data["priority"]] < min_prio:
                    continue

                # Print header if needed
                if first_item:
                    fd.write("\n")
                    fd.write("## %s\n" % section_name)
                    first_item = False

                # Print item
                ok &= process_checklist_item(mh, fd,
                                             steps,
                                             obj.location, obj.name, data)

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
