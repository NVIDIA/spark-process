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
import re
import argparse
import typing

from trlc.trlc import Source_Manager
from trlc.errors import Message_Handler

import common


def oxford_comma_and(strings):
    assert isinstance(strings, typing.Iterable)
    str_list = list(strings)
    assert all(isinstance(item, str) for item in str_list)
    assert len(str_list) >= 1

    if len(str_list) == 1:
        return str_list[0]

    else:
        return ", ".join(str_list[:-1]) + \
            ", and " + str_list[-1]


def link_gp_assumption(gnatprove_assumption):
    assert isinstance(gnatprove_assumption, str)
    name = gnatprove_assumption.split(".")[-1]
    return ":ref:`%s`" % name.lower().replace("_", "-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir")
    options = ap.parse_args()

    mh = Message_Handler()
    sm = Source_Manager(mh)

    sm.register_file(os.path.join(options.source_dir,
                                  "steps.rsl"))
    sm.register_file("spark-assumptions.rsl")
    sm.register_file("spark-assumptions.trlc")
    sm.register_file("tracing.rsl")
    sm.register_file("tracing.trlc")

    stab = sm.process()

    if stab is None:
        sys.exit(1)

    pkg_asm    = stab.lookup_assuming(mh, "Gnatprove_Assumptions")
    pkg_arg    = stab.lookup_assuming(mh, "Tracing")
    t_asm_kind = pkg_asm.symbols.lookup_assuming(mh, "Kind")

    ok = True
    for assumption_kind in t_asm_kind.literals.values():
        with open("tracing-%s.inc" % assumption_kind.name.lower(),
                  "w",
                  encoding="UTF-8") as fd:
            for assumption in pkg_asm.symbols.iter_record_objects():
                data = assumption.to_python_dict()
                if assumption.field["kind"].value is not assumption_kind:
                    continue

                fd.write(".. _%s:\n\n" %
                         assumption.name.lower().replace("_", "-"))
                fd.write(assumption.name + "\n")
                fd.write("^" * len(assumption.name) + "\n\n")
                fd.write("Description:\n\n")
                for line in data["text"].splitlines():
                    line = re.sub(r"\[\[(.*?)\]\]",
                                  lambda m: link_gp_assumption(m.group(1)),
                                  line)
                    fd.write("  %s" % line + "\n")

                fd.write("\n\n")

                found_tracing = False

                for arg in pkg_arg.symbols.iter_record_objects():
                    if arg.field["assumption"].target is not assumption:
                        continue

                    found_tracing = True
                    t_data = arg.to_python_dict()

                    if t_data["deferred_to"]:
                        fd.write("See entries for: %s\n\n" %
                                 oxford_comma_and(
                                     link_gp_assumption(item)
                                     for item in t_data["deferred_to"]))
                    else:
                        items = []
                        if t_data["via_process_assumptions"]:
                            items.append("(Process Assumptions)")
                        if t_data["process"]:
                            items += [common.fmt_step_link(item)
                                      for item in t_data["process"]]

                        if len(items) == 1:
                            fd.write("Applicable process step: %s\n\n" %
                                     items[0])
                        else:
                            assert len(items) > 1
                            fd.write("Applicable process steps:\n\n")
                            for step in items:
                                fd.write("  * %s\n" % step)
                            fd.write("\n")

                    if t_data["text"] is not None:
                        fd.write(t_data["text"] + "\n\n")

                if not found_tracing:
                    mh.warning(assumption.location,
                               "not traced in process")
                    fd.write(".. warning::\n\n")
                    fd.write("   Assumption not traced in process.\n\n")
                    ok = False

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
