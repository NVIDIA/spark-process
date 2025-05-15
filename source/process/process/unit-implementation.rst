.. Copyright (C) 2024 - 2025 NVIDIA CORPORATION & AFFILIATES
.. Copyright (C) 2021 - 2024 AdaCore
..
.. Permission is granted to copy, distribute and/or modify this document
.. under the terms of the GNU Free Documentation License, Version 1.3 or
.. any later version published by the Free Software Foundation; with the
.. Invariant Sections being "Attribution", with no Front-Cover
.. Texts, and no Back-Cover Texts.  A copy of the license is included in
.. the section entitled "GNU Free Documentation License".

Unit Implementation
-------------------

.. _step-create-adb:

Create ADB
^^^^^^^^^^

For each non-nested package implemented by the unit (as determined in
the :ref:`step-identify-external-packages` and
:ref:`step-identify-internal-packages` steps and recorded in the
Software Unit Verification Plan), identify whether the package
specification in the ADS file requires a package body (as determined
by :lrm:`7-1` and :lrm:`7-2`), and indicate in the Software Unit
Verification Plan whether the package requires a package body and (if
so) the corresponding ADB file name per the GNAT default file naming
convention.

For each non-nested package implemented by the unit that requires a
package body, create an ADB file for the package body. This can be
done either manually, or through GNATstub with a command such as:

.. code-block:: bash

   gnatstub -P my_unit_project

where ``my_unit_project`` is the name of the project file created in
the :ref:`step-create-project-file` step.

Ensure that each ADB file or its containing directory is identified as
source code in the unit project file.

Step ID: Create_ADB

.. _step-define-spark-package:

Define SPARK Package
^^^^^^^^^^^^^^^^^^^^

For each ADB file, declare the corresponding package body. Adding an
aspect declaration that sets ``SPARK_Mode`` to ``On`` is strongly
recommended, e.g.:

.. code-block:: ada

   package body My_Unit_Name.My_Child_Name
   with SPARK_Mode => On
   is

      ...

   end My_Unit_Name.My_Child_Name;

Note: This process permits package bodies to be declared with
``SPARK_Mode => Off`` or ``Annotate => (GNATprove, Skip_Proof)`` or
``Annotate => (GNATprove, Skip_Flow_And_Proof)``, but you should not
start out that way. See the note at the end of the
:ref:`step-implement-spark-package` step, below. If SPARK is disabled or proof is
skipped for the package body, then the software unit is not clean
SPARK, and if the software unit design process steps
(:ref:`step-document-design-solutions` and :ref:`step-inspect-unit-design`, in particular)
were executed on the assumption that the software unit is clean SPARK,
then those steps need to be revisited.

Step ID: Define_SPARK_Package

.. _step-implement-spark-package:

Implement SPARK Package
^^^^^^^^^^^^^^^^^^^^^^^

For each ADB file, provide full type declarations for all incomplete
type declarations in the private part of the corresponding ADS file,
and populate the bodies of all the procedures and functions.

Note: Developers should typically implement the simplest functions and
procedures first, then implement increasingly complex functions and
procedures. For example, functions and procedures with loops should be
added at the end. This supports an iterative process in which
GNATprove is often run, making it more likely that errors will be
caught as soon as they are introduced.

Make sure that the implementation compiles without errors or warnings.

While you are implementing functions and procedures, verify them one
by one using GNATprove. The ``--limit-subp`` switch allows doing this
limited verification. For example, if you want to verify a function
that has been declared at line 54 of the file
my_unit_name-my_child_name.ads, the command will be:

.. code-block:: bash

   gnatprove -P my_unit_project --limit-subp=my_unit_name-my_child_name.ads:54

Note that this can also be achieved by calling the "Prove Subprogram"
menu in GNAT Studio, while the focus is in the code of the subprogram.

In verifying each subprogram with GNATprove, the objective is to reach
zero warnings, zero errors, and zero low / medium / high check
messages. Refer to the subsections of this step for guidance on how to
achieve this.

Note: GNATprove may issue info messages depending on the configuration
(e.g. if switches ``--info`` or ``--report=all`` are used), but
eliminating info messages is not an objective.

Step ID: Implement_SPARK_Package

Non-SPARK Ada
"""""""""""""

If a subprogram body cannot be written in SPARK because the subprogram
body needs to use an Ada language feature forbidden in SPARK, then
mark the subprogram body as ``SPARK_Mode => Off``, supply a comment
justifying the decision to disable SPARK, and unsuppress all
language-defined checks before the first declaration or statement of
the body:

.. code-block:: ada

   -- SPARK_Mode is disabled for P because it calls functions that are
   -- declared with SPARK_Mode => Off.
   procedure P
   with SPARK_Mode => Off
   is
       pragma Unsuppress (All_Checks);
       ...
   begin
       ...
   end P;

If a non-SPARK subprogram body accesses any global variables, the
justifying comment must explain why it is necessary to access global
variables. (This is necessary for compliance with :ref:`ISO
26262-6:2018, Table 6, row 1e <iso-trace-p6-c8-4-5-t6-1e>`.)

If a non-SPARK subprogram body calls other subprograms, all the
outputs and return values must be consumed or explicitly discarded,
and all documented error cases must be handled by the calling
subprogram (:ref:`ISO 26262-6:2018 8.4.5f <iso-trace-p6-c8-4-5-f>`).

Non-SPARK code must be contained within ``pragma Unsuppress
(All_Checks)`` regions to ensure that all language-defined checks are
enabled at run time, since GNATprove will not be formally verifying
that the checks will pass. Non-SPARK code may include check
suppressions to locally disable specific checks (e.g., if a particular
contract cannot be executed), but if the ASIL of the software unit is
ASIL C or ASIL D, then you must manually implement defensive checks to
replace the disabled checks in order to comply with :ref:`ISO
26262-6:2018, Table 1, row 1d <iso-trace-p6-c5-4-3-t1-1d>` (which
highly recommends the "Use of defensive implementation techniques" at
ASILs C and D).

This process also permits entire package bodies to be declared with
``SPARK_Mode => Off``. However, doing so will increase the cost of
verification in later steps and can reduce performance due to the
requirement in this process to unsuppress language-defined checks in
``SPARK_Mode => Off`` code. Therefore:

* You should set ``SPARK_Mode => Off`` on a package body only if you
  need to declare package-body entities (types, global variables,
  etc.) not allowed in SPARK, on which you can't specify the
  ``SPARK_Mode => Off`` aspect individually, as you can with
  subprogram bodies.

* You should also move any SPARK-compliant entities out of the
  ``SPARK_Mode => Off`` package, wherever possible.

* You must preface a package body marked with ``SPARK_Mode => Off``
  with a comment justifying the decision to disable SPARK_Mode, as you
  must do for a subprogram body with ``SPARK_Mode => Off``.

* The justification comment should state why the non-SPARK package
  body is minimal: for example, if the package body contains
  subprograms, this justification must state why the full package body
  had to have ``SPARK_Mode => Off`` rather than just subprograms.

Proof Suggestions
"""""""""""""""""

If GNATprove cannot prove a verification condition within the allotted
time, then consider the following resolutions:

* Increase the number of steps allowed for proof.
* You may want to consider adding loop invariants and/or lemmas to
  prevent the prover from taking too long.
* Strengthen the subprogram specification's precondition.

  * Note: Only do this if the new, stronger precondition is still
    expected to be satisfied by all callers.

* Weaken the subprogram specification's postcondition and/or other
  contracts.

  * Note: Only do this if the new, weaker postcondition or other
    contract is still sufficient for all callers.

* Add additional code annotations in the form of assertion pragmas
  (``pragma Assert``, ``pragma Loop_Invariant``, or ``pragma
  Loop_Variant``) or ghost code computation.

  * Note: The objective of this resolution is to help GNATprove
    "understand" the connection between the subprogram preconditions
    and the subprogram postconditions and other subprogram
    contracts. Sometimes it is too big a leap for GNATprove to compute
    this without developer assistance.

* Modify the implementation to lower the degree of complexity, and/or
  split the subprogram into several smaller subprograms.

  * Note: The objective of this resolution is to make it easier for
    GNATprove to analyze the implementation.

Diagnostic Justifications
"""""""""""""""""""""""""

If none of the above resolutions are sufficient, select one of the
following resolutions. Be mindful that these latter resolutions will
result in additional manual verification work in subsequent steps
(such as the :ref:`step-review-diagnostic-justifications` step), and that these
resolutions are only appropriate if GNATprove has not identified any
counterexamples that prove the subprogram body is incorrect.

* Use ``pragma Assume (condition, justification);`` to direct
  GNATprove to assume a condition that GNATprove is unable to
  prove. Supply a justification (which will be reviewed as part of the
  global peer review in the :ref:`step-review-diagnostic-justifications` step)
  that indicates both why the assumption is valid and why it cannot be
  proven.

  * Note: When using ``pragma Assume``, developers should specify the
    assumed condition to be as weak as possible, so that GNATprove is
    leveraged to the greatest extent possible and the manual
    verification work is minimized.

  * Note: Except where pragma Assertion_Policy is used to override
    this, each pragma Assume is implicitly tested in the
    :ref:`step-verify-dynamic-assumptions` step, since the ``-gnata`` compiler
    option causes run-time checking of ``pragma Assume`` conditions.

* To suppress a particular check message, use ``pragma Annotate
  (GNATprove, False_Positive, check_message, justification);`` or
  ``pragma Annotate (GNATprove, Intentional, check_message,
  justification);``. Supply a justification (which will be reviewed as
  part of the global peer review in the
  :ref:`step-review-diagnostic-justifications` step) that indicates both why the
  suppression is valid and why the suppression is necessary.

* To suppress a particular warning message, surround the offending
  line(s) of code with ``pragma Warnings (GNATprove, Off,
  warning_message, Reason => justification);`` and ``pragma Warnings
  (GNATprove, On, warning_message);``. Supply a justification (which
  will be reviewed as part of the global peer review in the
  :ref:`step-review-diagnostic-justifications` step).

* If the subprogram specification does not include a
  ``Forward_Progress`` user aspect or an ``Always_Terminates`` aspect,
  or if it does include an ``Exceptional_Cases`` contract, add
  defensive code to dynamically check non-proven parts of the
  postcondition (GNATprove should be able to prove the postcondition
  once that defensive code is added).

  * Note: In the event the check fails, an error must be reported by
    some means outside the scope of this process, in lieu of
    returning. That is why this approach is not valid for subprograms
    with a ``Forward_Progress`` user aspect or ``Always_Terminates`` aspect
    unless they have an ``Exceptional_Cases`` aspect.

* Annotate the subprogram body with aspect ``Annotate => (GNATprove,
  Skip_Proof)`` or ``Annotate => (GNATprove, Skip_Flow_And_Proof)``,
  unsuppress all checks as described above for ``SPARK_Mode => Off``
  subprograms, and add a comment before the subprogram body justifying
  the decision to skip proof for the subprogram.

  * Note: This is a heavy approach that can suppress a large number of
    diagnostics. The justification must explain why it is not
    reasonable to suppress specific diagnostics as described in the
    preceding bullets. In addition, all the requirements for non-SPARK
    code apply equally to code for which proof is disabled.

Assign a unique ID to each diagnostic justification (refer to the
:ref:`step-review-diagnostic-justifications` step), by using a structured comment
as specified in the Traceability Model section. For example:

.. code-block:: ada

   -- @justify (In_Live_State)
   pragma Assume (In_Live_State, "We know it is live because...");

Note: Using pragma Assume/Annotate/Warnings as described above,
marking subprograms as ``SPARK_Mode => Off``, or marking subprograms
as ``Annotate => (GNATprove, Skip_Proof)`` or ``Annotate =>
(GNATprove, Skip_Flow_And_Proof)`` significantly reduces the
confidence of the overall proof, as the prover will believe the stated
properties without proving them. To the extent that it is not
hindering development of another part of the proof, these resolutions
should be avoided as much as possible.

Clean SPARK
"""""""""""

If ``SPARK_Mode`` is disabled for a subprogram or any diagnostic
justifications are used, then the software unit is by definition not
clean SPARK. If the software unit design process steps
(:ref:`step-document-design-solutions` and :ref:`step-inspect-unit-design`, in particular)
were executed on the assumption that the software unit is clean SPARK,
then revisit those steps.

Non-Formally-Verified Unit Specification Fragments
""""""""""""""""""""""""""""""""""""""""""""""""""

If a subprogram is annotated ``Annotate => (GNATprove, Skip_Proof)``
or ``Annotate => (GNATprove, Skip_Flow_And_Proof)``, or if
``SPARK_Mode`` is disabled for a subprogram, then the subprogram's
formal requirements or formal design constraints (if any) are by
definition non-formally-verified. If the software unit design process
steps (:ref:`step-capture-unit-design-constraints` and :ref:`step-document-design-solutions`,
in particular) were executed on the assumption that a particular
subprogram's formal requirements and formal design constraints were
going to be formally-verified, then revisit those steps.

.. _step-compile-project:

Compile Project
^^^^^^^^^^^^^^^

Build the project:

.. code-block:: bash

   gprbuild -P my_unit_project additional_switches

where my_unit_project is the name of the project as created in the
:ref:`step-create-project-file` step and additional_switches includes zero or more
non-compiler switches (e.g., switches controlling the quantity of CPU
resources that may be used for the build).

Note: Including compiler switches in additional_switches could result
in violation of GNATprove assumption [SPARK_COMPILATION_SWITCHES].

Record the precise command executed, its console output, and its exit
status in the Software Unit Verification Report.

Pass Criteria: compilation succeeds without errors, warnings, or style
messages. (Alternatively, you can just check that gprbuild exited with
a zero exit status.)

Step ID: Compile_Project
