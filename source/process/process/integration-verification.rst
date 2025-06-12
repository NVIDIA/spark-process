.. Copyright (C) 2024 - 2025 NVIDIA CORPORATION & AFFILIATES
.. Copyright (C) 2021 - 2024 AdaCore
..
.. Permission is granted to copy, distribute and/or modify this document
.. under the terms of the GNU Free Documentation License, Version 1.3 or
.. any later version published by the Free Software Foundation; with the
.. Invariant Sections being "Attribution", with no Front-Cover
.. Texts, and no Back-Cover Texts.  A copy of the license is included in
.. the section entitled "GNU Free Documentation License".

Integration Verification
------------------------

This process is about unit development. However, some verification
needs to be done on the entire program, and this section describes
verification activities to be delayed until integration time.

Note: While the process to a large extent fulfills the expectations in
ISO 26262 for the Verification Plan and Verification Specification for
software units developed in Ada, this process does not aim to do the
same for the Verification Plan and Verification Specification for
integration. This process merely assumes that the steps in this
section are part of the Verification Plan and/or Verification
Specification for integrated software that incorporates software units
developed according to this process.

.. _step-check-stack-usage-integration:

Check Stack Usage (Integration)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For each fully-linked program that incorporates one or more software
units developed according to this process, ensure that the amount of
primary stack space that the program needs does not exceed the amount
of primary stack space provided by the execution environment.

Note: This process does not prescribe a specific approach for ensuring
this, but the subsections of this step offer some suggestions.

Pass Criteria: Each execution environment provides sufficient primary
stack space for each fully-linked program that executes within that
execution environment.

Step ID: Check_Stack_Usage_Integration

Approach: Primary Stack Guard Regions
"""""""""""""""""""""""""""""""""""""

One approach is simply to run integration tests that exercise each
fully-linked program in a manner that uses the maximum amount of stack
space. If the program doesn't terminate due to an attempt to access a
primary stack guard region, then there is sufficient stack space.

Approach: Stack Usage High Water Mark Measurement
"""""""""""""""""""""""""""""""""""""""""""""""""

Another approach is to measure the maximum stack space used in each
thread across all integration tests. For example, you could use the
following algorithm:

* Repeat until all integration tests have been run:

  * For each stack, initialize all memory locations in the stack to a
    fixed pattern (such as 0xf00dcafe).
  * Run a subset of the integration tests.
  * For each stack:

    * Determine the lowest address of any memory location that does
      not contain the fixed pattern.
    * Subtract that address from the address of the top of the stack
      (the address one higher than the highest-addressed memory
      location of the stack).
    * Save this difference. It is the amount of space used on this
      stack for this subset of integration tests.

* For each stack:

  * Calculate the maximum of all the differences saved across all the
    integration test subsets.
  * This maximum is the amount of space used in this stack.

Check the maximum stack usage against the stack sizes configured in
the environment in which the integrated program executes. If the
maximum stack usage exceeds the allowed stack size:

* Consider alternative compilation options specifically during
  compilation of the object files that use the most stack space. For
  example, while none of the recommended optimization levels
  specifically optimize code for stack utilization, varying
  optimization levels can nevertheless impact stack utilization.

  * Note: This process recommends against using the
    ``-fomit-frame-pointer`` option. While this option often slightly
    reduces stack utilization, this option can also have a
    significantly negative impact on the debuggability of all the
    software linked into the same software partition (e.g., the same
    POSIX process).

* Consider adjusting stack size requirements to better accommodate the
  program's apparent stack needs.

ASIL of Availability
""""""""""""""""""""

As stated in the general assumptions, this process assumes that there
are no requirements for availability with ASILs greater than
ASIL B. At higher ASILs, :ref:`ISO 26262-6:2018, Table 1, row 1d
<iso-trace-p6-c5-4-3-t1-1d>` highly recommends the use of defensive
implementation techniques, so if there were such an availability
requirement, this process would need to mandate one of the following:

* Defensive techniques for managing the risk of stack overflow and
  recovering
* Prevention measures for ensuring the stack cannot possibly overflow

Impact of Compiler Switches
"""""""""""""""""""""""""""

Stack usage is heavily impacted by compiler switches. It is crucial
that this step be executed using the same compiler switches as those
used for production builds. For example, since production builds do
not use the ``-gnata`` switch (the use of the ``-gnata`` switch for
production builds is prohibited by this process), the ``-gnata``
switch must not be used in the build analyzed in this step
either. (See note in the :ref:`step-verify-dynamic-assumptions` section about the
potential impact of ``-gnata`` on stack utilization.)

.. _step-automated-check-against-coding-std-integration:

GNATcheck and gnatkp on whole program
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the Ada/SPARK Guidelines mandate any GNATcheck rules that perform
global analysis, then for each library or program that is built as
part of software integration, run GNATcheck to verify that the written
code is compliant with the coding standard defined in the Ada/SPARK
Guidelines:

.. code-block:: bash

   gnatcheck -P my_integration_project -U additional_switches

where my_integration_project is the name of a project that includes
all the ADS and ADB files of the library or program and
additional_switches consists of zero or more additional GNATcheck
switches.

The GNATcheck switches specified in my_integration_project and the
GNATcheck switches specified on the gnatcheck command line must enable
all the global analysis GNATcheck rules mandated by the Ada/SPARK
Guidelines.

Note: Most GNATcheck rules do not perform a global analysis; most
GNATcheck rules identify the same rule violations whether GNATcheck is
executed once on a whole program or GNATcheck is executed several
times on various pieces of the program. Such GNATcheck rules are
already fully enforced in the :ref:`step-automated-check-against-coding-std` step
and do not need to be checked here. However, there are some GNATcheck
rules, such as Deeply_Nested_Inlining, Recursive_Subprograms, and
Same_Instantiations that perform a global analysis. If the Ada/SPARK
Guidelines prescribe that any such rules are used, the Ada/SPARK
Guidelines may require GNATcheck to be run on the whole program.

Note: None of the GNATcheck rules mandated in the Requirements
Concerning GNATcheck Switches and Rules section perform a global
analysis. It is only necessary to run GNATcheck on the whole program
if required by the Ada/SPARK Guidelines.

Run GNATkp to verify that the written code is compliant with the GNAT
safety manual:

.. code-block:: bash

   gnatkp -P my_integration_project --kp-version=my_gnat_version

Where my_gnat_version is the version of the GNAT tools being used
(e.g., 24.0).

Alternatively, if running GNATkp on each whole program is not
possible, then the following can be done instead:

* Use GNATkp and/or its documentation to identify which GNATkp rules
  perform a global analysis.
* Manually check that each whole program complies with each such
  GNATkp rule.

Note: There have historically been known problems in GNAT tools,
detected by GNATkp, that involve certain kinds of legal but
unsupported inconsistencies between compilation units, but GNATkp can
only detect such known problems if it is given simultaneous visibility
into the compilation units containing the inconsistency.

Pass Criteria: GNATcheck (if required by the Ada/SPARK Guidelines) and
GNATkp (or manual analysis) report no warnings or coding standard or
safety manual violations.

Note: It is not sufficient to check that gnatcheck and gnatkp exited
with exit code 0, because they do this even if they emit warnings.

Step ID: Automated_Check_Against_Coding_Std_Integration

.. _step-static-analysis-integration:

Static Analysis (Integration)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For each library or program that is built as part of software
integration, optionally run CodePeer to analyze the code of the
program or library. Use command line switches that meet the criteria
defined in the :ref:`step-static-analysis-unit` step, except direct CodePeer to
analyze the project for the entire library or program, not the project
file(s) for the unit.

Note: This step is optional because CodePeer is a best-effort tool not
strictly relied upon by this process.

Pass Criteria: No medium/high message is present on non-proven Ada
code.

Step ID: Static_Analysis_Integration

.. _step-check-for-circular-dependencies:

Check for Circular Dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Verify through analysis of each program containing SPARK that the
program's GNATprove dependency graph is acyclic, where each program's
GNATprove dependency graph is defined as follows:

* The vertices of the program's GNATprove dependency graph are the
  project files of the program on which GNATprove was executed.
* For any two vertices P and Q of the program's GNATprove dependency
  graph, there is an edge from P to Q if and only if there exist
  compilation units A in P and B in Q such that B is a library unit
  declaration or library unit renaming declaration and A contains a
  with clause for B.

Pass Criteria: No cycles found.

Step ID: Check_For_Circular_Dependencies

.. _step-run-integration-tests:

Run Integration Tests
^^^^^^^^^^^^^^^^^^^^^

Run integration tests with production switches.

Then recompile and run unit tests with the project file modified as
follows:

* Ensure that the ``-gnata`` and ``-gnatVa`` compiler switches are
  present in ``Default_Switches ("Ada")`` in the ``Compiler`` package

* Ensure that the ``-gnatp`` and ``-gnato0`` compiler switches are not
  present in ``Default_Switches ("Ada")`` in the ``Compiler`` package

* Ensure that the file specified by ``Global_Configuration_Pragmas``
  in the ``Builder`` package includes ``pragma Initialize_Scalars``
  (if the Ada runtime used support it)

These modifications help ensure that in the presence of software units
not developed according to this process, all formal assumptions hold
at the boundaries between software units developed according to this
process and other software units.

If the Ada runtime does not support ``Initialize_Scalars``, then it is
necessary to rely on code inspection and static analysis to detect
uses of uninitialized variables in non-flow-analyzed code.

Note: See the note in the :ref:`step-verify-dynamic-assumptions` step concerning
the potential impact of ``-gnata`` and ``pragma Initialize_Scalars``
on stack and heap sizes.

Note: While integration testing is technically not a
software-unit-level activity, this step provides evidence of the
validity of assumptions that may have been made by this software unit
about other, non-platinum-proven software units.

Step ID: Run_Integration_Tests
