.. Copyright (C) 2024 - 2025 NVIDIA CORPORATION & AFFILIATES
.. Copyright (C) 2021 - 2024 AdaCore
..
.. Permission is granted to copy, distribute and/or modify this document
.. under the terms of the GNU Free Documentation License, Version 1.3 or
.. any later version published by the Free Software Foundation; with the
.. Invariant Sections being "Attribution", with no Front-Cover
.. Texts, and no Back-Cover Texts.  A copy of the license is included in
.. the section entitled "GNU Free Documentation License".

.. _sec-switches:

=====================================
Requirements Concerning Tool Switches
=====================================

For designated tools, this section specifies which tool switches must
be provided, and which tool switches must not be provided, when using
the tools per this process.

This section does not specify switches for tools not prescribed by
this process, such as the assembler, the binder, and the linker. These
tools are out of the scope of this process.

Requirements Concerning Compiler Warning Switches
-------------------------------------------------

This section specifies which compiler warning switches must be
provided, and which compiler warning switches must not be provided,
when compiling SPARK or Ada software per this process. Mandatory
compiler warning switches must be specified in the Compiler package of
each project file (unless the project sets Source_Files to
()). Prohibited compiler warning switches must not be specified in the
Compiler package of any project file.

This section also provides a rationale for why each warning switch is
required, prohibited, or neither.

This section covers every compiler warning switch documented in [GUG]_,
section Warning Message Control.

.. csv-table:: Required Compiler Warning Switches
   :header: "Switch", "Rationale for requiring"
   :widths: 2, 5
   :file: compiler_warning_required.csv

.. csv-table:: Prohibited Compiler Warning Switches
   :header: "Switch", "Rationale for prohibiting"
   :widths: 2, 5
   :file: compiler_warning_banned.csv

.. csv-table:: (Informative) Optional Compiler Warning Switches
   :header: "Switch", "Rationale for not requiring"
   :widths: 2, 5
   :file: compiler_warning_optional.csv

Requirements Concerning Non-Warning-Related Compiler Switches
-------------------------------------------------------------

This section specifies which non-warning-related compiler switches
must be provided, and which non-warning-related compiler switches must
not be provided, when compiling SPARK or Ada software per this
process. Mandatory non-warning-related compiler switches must be
specified in the Compiler package of each project file. Prohibited
non-warning-related compiler warning switches must not be specified in
the Compiler package of any project file.

This section also provides a rationale for why certain compiler
switches are required, prohibited, or neither.

Generally, switches that have been safety-qualified can be used where
their semantics match the requirements of a given project. Rationales
for permitting certain switches are listed below. Consult your safety
manual for a full list.

.. csv-table:: Required Compiler Switches
   :header: "Switch", "Rationale for requiring"
   :widths: 2, 5
   :file: compiler_required.csv

.. csv-table:: Prohibited Compiler Switches
   :header: "Switch", "Rationale for prohibiting"
   :widths: 2, 5
   :file: compiler_banned.csv

.. csv-table:: (Informative) Optional Compiler Switches
   :header: "Switch", "Rationale for not requiring"
   :widths: 2, 5
   :file: compiler_optional.csv


Requirements Concerning GNATprove Switches
------------------------------------------

This section specifies which GNATprove switches must be provided, and
which GNATprove switches must not be provided, when verifying SPARK
software per this process. Mandatory GNATprove switches must be
specified in the Prove package of each project file passed to
GNATprove or must be specified on each gnatprove command
line. Prohibited GNATprove switches must not be specified in the Prove
package of any project file passed to GNATprove and must not be
specified on the gnatprove command line.

This section also provides a rationale for why each GNATprove switch
is required, prohibited, or neither.

Note that this section has no bearing on the use of GNATprove outside
of the official verification of SPARK software per this process. As
part of normal development, it is permissible to use GNATprove with
prohibited switches and/or without mandatory switches, as long as
final verification is performed using switches consistent with this
section. Final verification refers to the gnatprove run in the Verify
Project step.

This section is intended to cover every GNATprove switch that is
documented in [SUG]_, section `Command Line Invocation
<https://docs.adacore.com/R/docs/gnat-25.1/spark2014/html/spark2014_ug/en/appendix/command_line_invocation.html>`_,
or documented via the output of `gnatprove --help`, excluding some
switches identified via the `gnatprove --help` output as "advanced
switches".

Any switch not listed here shall be assumed to be prohibited.

.. csv-table:: Required GNATprove Switches
   :header: "Switch", "Rationale for requiring"
   :widths: 2, 5
   :file: gnatprove_required.csv

.. csv-table:: Prohibited GNATprove Switches
   :header: "Switch", "Rationale for prohibiting"
   :widths: 2, 5
   :file: gnatprove_banned.csv

.. csv-table:: (Informative) Optional GNATprove Switches
   :header: "Switch", "Rationale for not requiring"
   :widths: 2, 5
   :file: gnatprove_optional.csv

Requirements Concerning GNATcheck Switches and Rules
----------------------------------------------------

This section specifies which GNATcheck switches [GCRM]_ must be
provided, and which GNATcheck switches must not be provided, when
verifying SPARK software per this process. Mandatory GNATcheck
switches must be specified in the Check package of each project file
passed to GNATcheck or on the gnatcheck command line. Any switch not
explicitly allowed here must not be specified in the Check package of
any project file passed to GNATcheck, and must not be passed on the
gnatcheck command line.

This section also provides a rationale for why each GNATcheck switch
is required, or optional.

Note that this section has no bearing on the use of GNATcheck outside
of the official verification of SPARK software per this process. As
part of normal development, it is permissible to use GNATcheck with
prohibited switches and/or without mandatory switches, as long as
final verification is performed using switches consistent with this
section.

Note: The Ada/SPARK Guidelines may mandate the use of additional
GNATcheck rules. This section is not intended to specify all desirable
GNATcheck rules, but rather is intended to specify what is minimally
required by this process. This section is not intended to specify a
coding standard.

.. csv-table:: Required GNATcheck Switches
   :header: "Switch", "Rationale for requiring"
   :widths: 2, 5
   :file: gnatcheck_required.csv

.. csv-table:: (Informative) Optional GNATcheck Switches
   :header: "Switch", "Rationale for not requiring"
   :widths: 2, 5
   :file: gnatcheck_optional.csv

.. csv-table:: Required GNATcheck Rules
   :header: "Switch", "Rationale for requiring"
   :widths: 2, 5
   :file: gnatcheck_required_rules.csv
