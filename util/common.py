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


PRIO_TO_NUMBER = {
    "All"    : 0,
    None     : 0,
    "Low"    : 1,
    "Medium" : 2,
    "High"   : 3,
}


def fmt_step_link(step):
    assert isinstance(step, str)

    if step in ("ALL", "VARIOUS"):
        return "*(%s)*" % step.capitalize()
    else:
        return ":ref:`%s <step-%s>`" % (step,
                                        step.lower().replace("_", "-"))


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
