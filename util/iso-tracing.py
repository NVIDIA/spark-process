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
from trlc.errors import Message_Handler, TRLC_Error
from trlc import ast

import common

def pp_iso_section(n_obj):
    assert isinstance(n_obj, ast.Record_Object)
    assert n_obj.n_typ.name == "Tracing"

    ref = n_obj.field["ref"]
    assert isinstance(ref, ast.Tuple_Aggregate)

    return "Section %u.%u" % (ref.value["chapter"].value,
                              ref.value["sec"].value)


def pp_iso_ref(n_obj, with_subref=True):
    assert isinstance(n_obj, ast.Record_Object)
    assert n_obj.n_typ.name == "Tracing"

    ref = n_obj.field["ref"]
    assert isinstance(ref, ast.Tuple_Aggregate)

    rv = "Part %u - Section %u" % (ref.value["part"].value,
                                   ref.value["chapter"].value)
    if isinstance(ref.value["sec"], ast.Integer_Literal):
        rv += ".%u" % ref.value["sec"].value

        if isinstance(ref.value["subsec"], ast.Integer_Literal):
            rv += ".%u" % ref.value["subsec"].value

            if isinstance(ref.value["subsubsec"], ast.Integer_Literal):
                rv += ".%u" % ref.value["subsubsec"].value

    if with_subref and isinstance(n_obj.field["subref"], ast.String_Literal):
        rv += " %s" % n_obj.field["subref"].value

    return rv


def pp_step_id(n_step):
    assert isinstance(n_step, ast.Enumeration_Literal_Spec)
    return common.fmt_step_link(n_step.name)


def get_process_steps(n_obj):
    assert isinstance(n_obj, ast.Record_Object)
    assert n_obj.n_typ.name == "Tracing"

    rv = []

    if isinstance(n_obj.field["steps"], ast.Array_Aggregate):
        rv += [pp_step_id(item.value)
               for item in n_obj.field["steps"].value]

    if isinstance(n_obj.field["ref_steps"], ast.Array_Aggregate):
        rv += ["See :ref:`%s <iso-trace-%s>`" %
               (pp_iso_ref(ref.target),
                ref.target.name.replace("_", "-"))
               for ref in n_obj.field["ref_steps"].value]

    return rv


def process(mh, fd, n_obj, emit_steps):
    assert isinstance(mh, Message_Handler)
    assert isinstance(n_obj, ast.Record_Object)
    assert isinstance(emit_steps, bool)

    fd.write(".. _iso-trace-%s:\n\n" % n_obj.name.replace("_", "-"))

    fd.write(".. topic:: %s:\n\n" % pp_iso_ref(n_obj))
    if isinstance(n_obj.field["text"], ast.String_Literal):
        for line in n_obj.field["text"].value.splitlines():
            line = "  " + line
            fd.write(line.rstrip() + "\n")
        fd.write("\n")

    if isinstance(n_obj.field["row"], ast.String_Literal):
        lines = n_obj.field["row"].value.splitlines()
        if len(lines) == 1:
            actual_row = lines[0]
            notes      = None
        else:
            if len(lines) < 3:
                mh.error(n_obj.field["row"].location,
                         "must be 1 or 3+ lines long")
            actual_row = lines[0]
            assert lines[1].strip() == ""
            notes      = lines[2:]

        fd.write("  .. list-table::\n")
        fd.write("     :widths: 10 1 1 1 1\n")
        fd.write("     :header-rows: 1\n")
        fd.write("\n")
        fd.write("     * -\n")
        fd.write("       - A\n")
        fd.write("       - B\n")
        fd.write("       - C\n")
        fd.write("       - D\n")
        fd.write("     * - %s\n" % actual_row)
        for asil in "ABCD":
            if asil.lower() in n_obj.field["applies"].value:
                fd.write("       - ``+``\n")
            elif asil in n_obj.field["applies"].value:
                fd.write("       - ``++``\n")
            else:
                fd.write("       - ``o``\n")
        fd.write("\n")

        if notes is not None:
            for line in notes:
                line = "  " + line
                fd.write(line.rstrip() + "\n")
            fd.write("\n")

    if emit_steps:
        fd.write("Process steps that apply:")
        steps = get_process_steps(n_obj)
        if len(steps) == 0:
            if isinstance(n_obj.field["alt_steps"], ast.Implicit_Null):
                fd.write(" N/A\n\n")
            else:
                fd.write("\n\n")
        elif len(steps) == 1:
            fd.write(" %s\n\n" % steps[0])
        else:
            fd.write("\n\n")
            for step in steps:
                fd.write("* %s\n" % step)
            fd.write("\n")

        if isinstance(n_obj.field["alt_steps"], ast.String_Literal):
            for line in n_obj.field["alt_steps"].value.splitlines():
                line = "  " + line
                fd.write(line.rstrip() + "\n")
            fd.write("\n")

    if isinstance(n_obj.field["same_as"], ast.Record_Reference):
        target = n_obj.field["same_as"].target
        fd.write("Same as: :ref:`%s <iso-trace-%s>`\n\n" %
                 (pp_iso_ref(target),
                  target.name.replace("_", "-")))

    if isinstance(n_obj.field["just"], ast.String_Literal):
        fd.write("Justification:\n\n")
        for line in n_obj.field["just"].value.splitlines():
            line = "  " + line
            fd.write(line.rstrip() + "\n")
        fd.write("\n")

    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs",
                    nargs="*",
                    help="input sources")
    ap.add_argument("--out",
                    default=None,
                    help="output rest file")
    ap.add_argument("--no-steps",
                    default=False,
                    action="store_true",
                    help="Omit step references (intended for guidelines)")

    options = ap.parse_args()

    mh = Message_Handler()
    sm = Source_Manager(mh)

    for filename in options.inputs:
        if not os.path.isfile(filename):
            ap.error("%s is not a file" % filename)
        sm.register_file(filename)

    stab = sm.process()

    if stab is None:
        sys.exit(1)

    ok = mh.errors == 0

    pkg_tracing = stab.lookup_assuming(mh, "ISO_26262_Tracing")

    old_section = None

    with open(options.out, "w", encoding="UTF-8") as fd:
        for item in pkg_tracing.symbols.iter_record_objects():
            current_section = pp_iso_section(item)
            if old_section != current_section:
                fd.write("%s\n" % current_section)
                fd.write("^" * len(current_section) + "\n\n")
                old_section = current_section

            try:
                ok &= process(mh, fd, item, not options.no_steps)
            except TRLC_Error:
                ok = False

    section_file = os.path.splitext(options.out)[0] + ".sections"
    with open(section_file, "w", encoding="UTF-8") as fd:
        for item in pkg_tracing.symbols.iter_record_objects():
            fd.write(pp_iso_ref(item, with_subref=False) + "\n")

    verbatim_file = os.path.splitext(options.out)[0] + ".verbatim"
    with open(verbatim_file, "w", encoding="UTF-8") as fd:
        for item in pkg_tracing.symbols.iter_record_objects():
            if isinstance(item.field["text"], ast.String_Literal):
                fd.write(item.field["text"].value + "\n")
            else:
                fd.write(item.field["row"].value + "\n")

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
