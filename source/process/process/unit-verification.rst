.. Copyright (C) 2024 - 2025 NVIDIA CORPORATION & AFFILIATES
.. Copyright (C) 2021 - 2024 AdaCore
..
.. Permission is granted to copy, distribute and/or modify this document
.. under the terms of the GNU Free Documentation License, Version 1.3 or
.. any later version published by the Free Software Foundation; with the
.. Invariant Sections being "Attribution", with no Front-Cover
.. Texts, and no Back-Cover Texts.  A copy of the license is included in
.. the section entitled "GNU Free Documentation License".

Unit Verification
-----------------

.. _step-develop-unit-verification-plan:

Develop Unit Verification Plan
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Complete the Software Unit Verification Plan (which specifies the plan
for verifying the software unit). This work product was initiated in
the :ref:`step-identify-activity-scope` step.

Note: Multiple software units can share the same Software Unit
Verification Plan document.

The Software Unit Verification Plan must comply with the following
constraints:

* It must identify the specific versions of the files containing the
  software unit design and implementation to be verified. Where
  possible, you should use Configuration Management features to
  minimize manual effort.

  * Note: The specific files containing the software unit design and
    implementation to be verified have already been recorded in the
    Software Unit Verification Plan in the :ref:`step-identify-activity-scope`,
    :ref:`step-identify-internal-packages`, and :ref:`step-create-adb` steps.

* It must specify the objectives of software unit verification. The
  stated objectives must include (but need not be limited to) the
  objectives identified in :ref:`ISO 26262-6:2018, 9.1
  <iso-trace-p6-c9-1-a>`.

* It must indicate that the verification methods, the verification
  pass/fail criteria, the verification environment, and some of the
  verification tools are defined in this document (the SPARK-Based ISO
  26262 Safety Process for Vehicle Software), including the particular
  version of this document that was used.

* It must identify any other tools or equipment used as part of
  verifying the software unit.

* It must identify the resources needed in order to perform the
  verification of the software unit.

* It must identify the actions to be taken if anomalies are detected
  during verification and the incremental re-verification required
  after changes to the software unit design and/or implementation.

This process specifies checklists to be used for verification. This
process mandates that if the answer to any yes/no checklist question
is anything other than an unequivocal "yes", then verification
fails. This is the root pass/fail criterion for software unit
verification done according to this process.

Pass Criteria: Software Unit Verification Plan has been developed and
satisfies all the above criteria.

Step ID: Develop_Unit_Verification_Plan

Automated Static Verification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _step-verify-project:

Verify Project
""""""""""""""

After the implementation is complete, official verification shall be
done using GNATprove:

.. code-block:: bash

   gnatprove -P my_unit_project --clean
   gnatprove -P my_unit_project -U additional_switches

where my_unit_project is the name of the project as created in the
:ref:`step-create-project-file` step and additional_switches consists of zero or
more additional GNATprove switches.

The first gnatprove command cleans intermediate files, which is
necessary to prevent the use of out-of-date results.

The GNATprove switches specified in my_unit_project and the GNATprove
switches specified on the second gnatprove command line must
collectively comply with the Requirements Concerning GNATprove
Switches section.

If the compilation units of a software unit are included in multiple
projects, then GNATprove must be invoked on each of the project
files. This addresses the risk explained in the Rationale For Invoking
On Each Project subsection.

Note: This step is a final check of :ref:`step-implement-spark-package` where each
individual subprogram has been proven before. Refer to the
:ref:`step-implement-spark-package` step for guidance on resolving any errors,
warnings, or check messages.

Record the precise commands executed, their console output, and their
exit statuses in the Software Unit Verification Report.

Pass Criteria: GNATprove reports no warnings, errors, or
low/medium/high check messages. (Alternatively, you can just check
that gnatprove exited with a zero exit status.) Warnings, errors, and
low/medium/high check messages, have the following formats,
respectively:

.. code-block:: text

   file:line:column: error: message
   file:line:column: warning: message
   file:line:column: low: message
   file:line:column: medium: message
   file:line:column: high: message

Step ID: Verify_Project

Rationale For Invoking On Each Project
''''''''''''''''''''''''''''''''''''''

Sometimes, in the course of verifying one software unit, GNATprove has
visibility into the unit design detail of other software units:

* External ADS files can include software unit implementation detail
  in their private parts.

* The :ref:`step-create-project-file` step allows the project to include ADS/ADB
  files that are not part of the software unit being verified.

Each of these allowances introduces a risk that in formally verifying
the software unit, GNATprove might utilize information about the
bodies of subprograms outside the scope of the software unit. If such
a situation were to occur, then the verification of the software unit
would be incomplete; GNATprove might not detect a systematic fault
consisting of an undocumented dependency of the software unit on
another software unit. However, there are two reasons why this risk is
acceptable.

First, the risk is mostly hypothetical, because GNATprove mostly
performs a subprogram-by-subprogram analysis. There are only a few
properties of subprograms that can be inferred from their bodies, such
as variables read/written (where Global aspects are missing),
termination (where Always_Terminates aspects, and No_Return aspects
are missing), whether a subprogram is "potentially blocking", and
absence of mutual recursion.

Second, even where GNATprove can infer properties of subprograms, this
cannot result in an invalid assumption being used for proof, because
(per this step) GNATprove must be invoked on each project that
contains compilation units from the software unit.

Suppose for example that:

* Software unit A calls a subprogram with multiple implementations:
* One implementation in unit B
* One implementation in unit C
* One implementation in unit D
* The project files are as follows:
* One project combines A and B
* A second project combines A and C
* A third project includes just A so that it can later be linked with D

Then:

* Invocation of GNATprove on the first project (containing A and B)
  enables GNATprove to leverage implementation detail of B in proving
  A in the context of B, but not implementation detail of C or D.
* Invocation of GNATprove on the second project (containing A and C)
  enables GNATprove to leverage implementation detail of C in proving
  A in the context C, but not implementation detail of B or D.
* Invocation of GNATprove on the third project (containing just A)
  does not enable GNATprove to leverage any implementation detail of
  B, C, or D in proving A.

Therefore, invoking GNATprove on each project that contains
compilation units from the software unit is sufficient to mitigate the
risk described in this subsection.

Consistency
'''''''''''

This step implicitly verifies the consistency of the formally-verified
unit requirements with the non-formally-verified requirements, because
if there were any contradiction between the formally-verified unit
requirements and the non-formally-verified unit requirements, it would
not be possible to specify a unit design and implementation that
satisfy both the formally-verified unit requirements and the
non-formally-verified unit requirements. This verification cannot be
done earlier as part of specifying the unit requirements for a
software interface, because at that point not all the unit
requirements are known (a single software unit might implement
multiple software interfaces, or receive requirements from other
sources such as the requirements management tool, software
architectural design, or hardware-software interface specifications).

Formal Verification of Generic Instantations
''''''''''''''''''''''''''''''''''''''''''''

When a generic package or subprogram is instantiated at an
instantiation site that is at a lower level of SPARK (Stone vs. Bronze
vs. Silver/Gold/Platinum) than part of the generic package or
subprogram declaration or body, the :ref:`step-write-tests` step requires a test
case for the instantiation to facilitate formal verification of the
instantiation, and the :ref:`step-formally-verify-test-cases` step requires that
formal verification.

In general, when this process refers to formal verification being done
in this step (the :ref:`step-verify-project` step), unless specified otherwise,
this process should be understood as referring to the formal
verification done in the :ref:`step-formally-verify-test-cases` step as well.

.. _step-automated-check-against-coding-std:

Automated Check Against Coding Standard and Safety Manual
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Run gnatcheck to verify that the written code is compliant with rules
specified in this process and with the coding standard defined in the
Ada/SPARK Guidelines:

.. code-block:: bash

   gnatcheck -P my_unit_project -U additional_switches

where my_unit_project is the name of the project as created in the
:ref:`step-create-project-file` step and additional_switches consists of zero or
more additional GNATcheck switches.

The GNATcheck switches specified in my_unit_project and the GNATcheck
switches specified on the gnatcheck command line must collectively
comply with the Requirements Concerning GNATcheck Switches and Rules
section below. In addition, the switches must collectively enable all
the GNATcheck rules mandated by the Ada/SPARK Guidelines.

Run gnatkp to verify that the written code is compliant with the GNAT
safety manual:

.. code-block:: bash

   gnatkp -P my_unit_project --kp-version=my_gnat_version

where my_gnat_version is the version of the GNAT tools being used
(e.g., 24.0).

Record the precise commands executed, their console output, and their
exit statuses in the Software Unit Verification Report.

Step ID: Automated_Check_Against_Coding_Std

.. _step-fix-coding-std-issues:

Fix Coding Standard and Safety Manual Violations
""""""""""""""""""""""""""""""""""""""""""""""""

In case violations are reported during coding standard and safety
manual review, eliminate them (in any preferred order) by doing one of
the following:

* Modify the code so that it follows the coding standard and safety
  manual.

  * For example, for a violation of GNATcheck rule
    ``Metrics_Cyclomatic_Complexity:10``, refactor the executable body
    to lower complexity or split it into several smaller subprograms.

* (For coding standard violations only) Add an annotation to justify
  the violation, e.g.:

  .. code-block:: ada

     -- @justify (local_id_for_justification)
     pragma Annotate (GNATcheck, Exempt_On, "Rule_Name", "justification");

     ...

     pragma Annotate (GNATcheck, Exempt_Off, "Rule_Name");

Note: Justifications will be reviewed as part of the global peer
review in the :ref:`step-review-diagnostic-justifications` step.

Pass Criteria: GNATcheck and GNATkp report no warnings or coding
standard or safety manual violations.

Note: It is important to check for warnings because GNATcheck can
issue warnings for serious issues, such as malformed exempted source
code sections and missing Exempt_Off annotations. Also, it is not
sufficient to check that gnatcheck and gnatkp exited with exit code 0,
because they do this even if they emit warnings.

Step ID: Fix_Coding_Std_Issues

.. _step-static-analysis-unit:

Static Analysis (Unit)
""""""""""""""""""""""

Note: As of the development of this section, the CodePeer command line
interface has not yet been determined. The expected functionality of
CodePeer is sufficiently well-defined to specify how CodePeer is to be
used, but you must use the CodePeer manual [GSAUG]_ to determine the
actual command line switches to use.

Run CodePeer to statically analyze the software unit code. Use the
command line switches as specified in the CodePeer documentation to
direct CodePeer to:

* Analyze all Ada source files in the project created in the
  :ref:`step-create-project-file` step.
* Suppress diagnostics in proven Ada code (``SPARK_Mode => On`` code
  for which proof is not disabled with the ``Skip_Proof`` or
  ``Skip_Flow_And_Proof`` annotations) but not in any non-proven Ada
  code.
* Suppress "low" diagnostics but not "medium" or "high" diagnostics.

If there are CodePeer messages pertaining to non-proven Ada code, then
those CodePeer messages must be (1) viewed and understood and then (2)
addressed. Only then can this step be retried.

For each medium/high CodePeer message pertaining to non-proven Ada
code, address the CodePeer message with one of the following
approaches:

* Correct any bugs in the code corresponding to the CodePeer message.
* Suppress the CodePeer message by placing one of the following
  immediately after the code that causes the CodePeer message:

  .. code-block:: ada

     pragma Annotate(CodePeer, False_Positive, check_name, justification);
     pragma Annotate(CodePeer, Intentional, check_name, justification);

  Supply a justification, which will be reviewed as part of the local
  peer review for in-context comprehensibility in the
  :ref:`step-inspect-implementation` step.

Note: Do not use ``pragma Annotate (CodePeer, Skip_Analysis)``. Each
medium/high CodePeer message in non-proven Ada code must be justified
individually.

Record the precise command executed, its console output, its exit
status, and the contents of all output files in the Software Unit
Verification Report. (Note: Output file contents can be incorporated
by reference.)

Pass Criteria: no medium/high message is present on non-proven Ada
code.

Step ID: Static_Analysis_Unit

Proven Code
'''''''''''

The risk reduction that would be achieved by investigating CodePeer
diagnostics concerning proven SPARK declarations or executable bodies
would be insignificant. GNATprove already formally verifies compliance
of SPARK declarations and executable bodies with formal
requirements. And CodePeer is typically not able to infer non-formal
requirements of SPARK declarations and executable bodies from context,
since SPARK specifications developed according to this process
typically formalize the sorts of requirements CodePeer is able to
infer.

Multiple Project Files
''''''''''''''''''''''

As explained in the :ref:`step-create-project-file` step, there may be multiple
unit project files that collectively cover the software unit, in which
case CodePeer would be invoked multiple times in this step, once per
unit project file. In this case, CodePeer will not have as much
visibility into interactions between different parts of the software
unit covered by different unit project files. However, this will be
rectified in the :ref:`step-static-analysis-integration` step, which takes an
integration project file as input. The main purpose of this process
step is to reduce the number of "new" CodePeer diagnostics that arise
in the :ref:`step-static-analysis-integration`, since it is more expensive to
analyze and address CodePeer diagnostics in an integrated context than
to analyze and address CodePeer diagnostics in a unit context.

.. _step-check-stack-usage-unit:

Check Stack Usage (Unit)
""""""""""""""""""""""""

Run GNATstack [GSUG]_ to analyze the units in your project:

.. code-block:: bash

   gnatstack -x -np -l 1000000 -P my_unit_project

Based on the GNATstack output, determine the median stack frame
size. Search the GNATstack output for subprograms with stack frame
sizes that are greater than five times the median stack frame
size. For each such subprogram:

* Verify that the software unit design identifies the specific
  subprogram by name as a subprogram potentially requiring a large
  amount of stack space.
* Verify that the software unit design provides a numerical upper
  bound on the stack frame size of the subprogram.
* Verify that the actual stack frame size reported by GNATstack does
  not exceed this upper bound.

Search the GNATstack output for subprograms with variable-length stack
frame sizes. For each subprogram, verify that the software unit design
identifies the specific subprogram by name as a subprogram potentially
requiring a variable-length stack frame.

If any of the above verification fails (if any unexpectedly large
stack frames and/or unexpected variable-length stack frames are
found), then either update the software unit design or improve the
efficiency of the code to use less stack space.

Record the precise command executed, its console output, its exit
status, and the contents of all output files in the Software Unit
Verification Report. (Note: Output file contents can be incorporated
by reference.)

Pass Criteria: GNATstack output shows no unexpectedly large stack
frames and shows no unexpected variable-length stack frames.

Step ID: Check_Stack_Usage_Unit

.. _sec-uv-manual-static-verification:

Manual Static Verification
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _step-review-diagnostic-justifications:

Review Diagnostic Justifications
""""""""""""""""""""""""""""""""

Conduct a global peer review of the diagnostic justifications provided
for any resolutions used to work around individual GNATprove or
GNATcheck diagnostics:

* Non-formally-verified assumptions, also known as GNATprove indirect
  justifications: `pragma Assume
  <https://docs.adacore.com/R/docs/gnat-25.1/spark2014/html/spark2014_ug/en/source/assertion_pragmas.html#pragma-assume>`_

* GNATprove warning suppressions: `pragma Warnings (GNATprove, Off/On,
  ...)
  <https://docs.adacore.com/R/docs/gnat-25.1/spark2014/html/spark2014_ug/en/source/how_to_use_gnatprove_in_a_team.html#suppressing-warnings>`_
  and ``pragma Warnings (Off/On, ...)``

* GNATprove check message direct justifications: `pragma Annotate
  (GNATprove, False_Positive/Intentional...)
  <https://docs.adacore.com/R/docs/gnat-25.1/spark2014/html/spark2014_ug/en/source/how_to_use_gnatprove_in_a_team.html#direct-justification-with-pragma-annotate>`_

* GNATcheck rule exemptions:
  ``pragma Annotate (GNATcheck, Exempt_On/Exempt_Off...)``

Note: This process does not depend on compiler warnings for safety. To
suppress a warning that only comes from the compiler, it is preferable
to use ``pragma Warnings (GNAT, Off/On, ...)`` instead of ``pragma
Warnings (Off/On, ...)``. The former pragma is not considered a
diagnostic justification, whereas the latter pragma is considered a
diagnostic justification, so there is less verification required for
the former pragma than for the latter pragma.

Global peer review of GNATprove assumptions (GNATprove indirect
justifications) must be done by searching for the presence of ``pragma
Assume`` in the source code.

GNATprove warning suppressions, GNATprove check message direct
justifications, and GNATcheck rule exemptions should be as precise as
possible about the specific diagnostic messages that they justify or
suppress. Typically, this means that:

* For warning suppression, a first ``pragma Warnings (GNATprove, Off,
  ...)`` should be used to start the suppression scope, which should
  end with a second ``pragma Warnings (GNATprove, On, ...)`` to
  restore warnings, and a specific string should be used to refer to
  the one warning being suppressed.

* A direct justification ``pragma Annotate`` should be inserted
  immediately after the statement or declaration to which the check
  message is attached, and a specific string should be used to
  identify the one check message being justified.

* For GNATcheck rule suppression, a first ``pragma Annotate
  (GNATcheck, Exempt_On, ...)`` should be used to start the exemption
  scope, which should end with a second ``pragma Annotate (GNATcheck,
  Exempt_Off, ...)`` to re-enable the rule.

Global peer review of warning suppression must be done by searching
for the presence of ``pragma Warnings (GNATprove, Off, ...)`` and
``pragma Warnings (Off, ...)`` in the source code.

Global peer review of GNATprove check message direct justifications
must be done either:

* By searching for the presence of ``pragma Annotate (GNATprove, X,
  ...)`` or aspect ``Annotate (GNATprove, X, ...)`` where X is
  ``Intentional`` or ``False_Positive``, in the source
  code. Alternately, these messages can be seen in the proof summary
  table in gnatprove.out, or

* By inspecting the GNATprove output (when ``--report=all`` is used to
  display info messages) or the GNATprove analysis log (in file
  gnatprove/gnatprove.out) for justified messages. Search for uses of
  the word justified.

Global peer review of GNATcheck rule exemptions must be done by
searching for the presence of ``pragma Annotate (GNATcheck...)`` in the
code.

In all cases, the global peer reviewer must evaluate the documented
justification and ensure all the following:

* The justification provides a convincing explanation that the
  GNATprove or GNATcheck diagnostic being worked around does not
  indicate the presence of a bug.

  * For a GNATcheck diagnostic, if the violated GNATcheck rule is
    listed as a mandatory rule in the Requirements Concerning
    GNATcheck Switches and Rules section, then this justification must
    consider the motivation for the GNATcheck rule documented in that
    section.

* The justification provides a convincing explanation that there was
  no straightforward way of addressing the GNATprove or GNATcheck
  diagnostic without resorting to a justification.

* The justification has a unique ID specified using structured
  comments with the syntax defined in the Traceability Model section.

In addition, for suppression of certain diagnostics, the global peer
reviewer must evaluate whether the code satisfies specific GNATprove
assumptions, as enumerated in the Traceability to GNATprove
Assumptions section of this document:

* GNATprove warnings classified as "guaranteed" per [SUG]_

  * assumed Always_Terminates

    * [PARTIAL_TERMINATION]

  * assumed Global null

    * [PARTIAL_GLOBAL]

  * imprecisely supported address specification

    * [SPARK_EXTERNAL]
    * [SPARK_ALIASING_ADDRESS]
    * [SPARK_EXTERNAL_VALID]

* Violations of GNATcheck rules motivated by GNATprove assumptions

  * Forbidden_Attributes:Initialized

    * [SPARK_INITIALIZED_ATTRIBUTE]

  * Restrictions:Max_Protected_Entries=>0

    * [SPARK_OVERRIDING_AND_TASKING].1b

      * Note: Violations of this restriction will be reported at each
        protected entry declaration, not at each of the call sites of
        each of the protected entries. To satisfy this GNATprove
        assumption, document an informal precondition for each
        protected entry that prohibits the protected entry from being
        called (directly or indirectly) from a dispatching call.

  * Restrictions:No_Floating_Point

    * [SPARK_FLOATING_POINT]

  * Restrictions:No_Protected_Types

    * [SPARK_OVERRIDING_AND_TASKING].1e

  * Restrictions:No_Specification_Of_Aspect=>Iterable

    * [SPARK_ITERABLE].1a
    * [SPARK_ITERABLE].1b
    * [SPARK_ITERABLE_FOR_PROOF].1a (for any Iterable_For_Proof
      annotation corresponding to the type with the Iterable aspect)
    * [SPARK_ITERABLE_FOR_PROOF].1b (for any Iterable_For_Proof
      annotation corresponding to the type with the Iterable aspect)

  * Restrictions:No_Use_Of_Entity=>Ada.Task_Identification.Current_Task

    * [SPARK_OVERRIDING_AND_TASKING].1f

  * Restrictions:No_Use_Of_Entity=>Synchronous_Task_Control

    * [SPARK_OVERRIDING_AND_TASKING].1c

Pass Criteria: As part of a global peer review, reviewers have
reviewed all the diagnostic justifications, ensured that they are
justified per the above criteria, and ensured that test cases have
been added to the Software Unit Verification Specification as
necessary to support the diagnostic justifications.

Step ID: Review_Diagnostic_Justifications

.. _step-review-deactivated-spark:

Review Deactivated SPARK
""""""""""""""""""""""""

Identify all subprograms, packages, tasks, and protected objects that
have ``SPARK_Mode`` disabled or ``Annotate => (GNATprove,
Skip_Proof)`` or ``Annotate => (GNATprove, Skip_Flow_And_Proof)``
annotations applied for part or all of their syntax. Look specifically
for the following Ada constructs:

* Any compilation unit that satisfies both of the following conditions:

  * The compilation unit is not based on either a
    generic_instantiation or a library_unit_renaming_declaration
    (ignoring the context_clause and optional private keyword).

  * The declaration or body on which the compilation unit is based
    does not have a ``SPARK_Mode`` aspect with no value or a
    ``SPARK_Mode => On`` aspect.

* Any Ada syntactic construct with a ``SPARK_Mode => Off`` aspect,
  ``pragma SPARK_Mode (Off)``, or the ``Annotate => (GNATprove,
  Skip_Proof)`` or ``Annotate => (GNATprove, Skip_Flow_And_Proof)``
  aspect.

Conduct a global peer review of all subprograms, packages, and other
entities that have ``SPARK_Mode`` disabled or ``Annotate =>
(GNATprove, Skip_Proof)`` or ``Annotate => (GNATprove,
Skip_Flow_And_Proof)`` annotations applied for part or all of their
syntax. For each such entity, manually verify in particular that all
the following criteria are met:

* Justification and Scope

  * There must be a comment before the entity justifying the decision
    to disable SPARK_Mode or skip proof, and the justification must
    provide a convincing explanation that there was no straightforward
    way to enable SPARK_Mode or proof for the entity.

* Packages

  * If the entity is all or part of a package specification or body,
    then the package must comply with all parts of GNATprove
    assumption [ADA_ELABORATION].
  * If the entity is the private part of a package specification or is
    all or part of a package body, the entity must comply with all
    parts of GNATprove assumptions [ADA_EXTERNAL_ABSTRACT_STATE] and
    [ADA_STATE_ABSTRACTION].

* Data and Types

  * If the entity accesses any global variables, the justifying
    comment must explain why it is necessary to access global
    variables. (This is necessary for compliance with :ref:`ISO
    26262-6:2018, Table 6, row 1e <iso-trace-p6-c8-4-5-t6-1e>`.)
  * If the entity contains accesses to objects shared with SPARK code,
    then each such case must comply with GNATprove assumptions
    [ADA_EXTERNAL] and [ADA_EXTERNAL_NAME].
  * For each type completion in the entity for a type that was
    declared in a SPARK entity, the completion must comply with all
    parts of GNATprove assumption [ADA_PRIVATE_TYPES].
  * For each type defined by the entity as an extension of a type
    declared in SPARK code, the type definition must comply with
    GNATprove assumption [ADA_TAGGED_TYPES].
  * For each value assigned by the entity to an object of recursive
    type, the value must comply with GNATprove assumption
    [ADA_RECURSIVE_TYPES].

* Subprograms

  * If the entity is or contains a subprogram called from SPARK code,
    then each such subprogram must comply with all parts of GNATprove
    assumption [ADA_SUBPROGRAMS], [ADA_OBJECT_ADDRESSES],
    [ADA_LOGICAL_EQUAL], and [ADA_INLINE_FOR_PROOF].
  * If the entity is or contains a call to a SPARK subprogram body,
    then each such call must comply with all parts of GNATprove
    assumption [ADA_CALLS].
  * If the entity is or contains a subprogram whose declaration is
    annotated with the ``No_Heap_Allocations`` or
    ``No_Secondary_Stack`` local restriction (whether directly, or
    indirectly via a ``Forward_Progress`` user aspect), then each
    subprogram and all subprograms called from it (whether directly or
    indirectly) must refrain from heap allocations or secondary stack
    allocations, respectively.
  * If the entity calls other subprograms, all the outputs and return
    values must be consumed or explicitly discarded, and all
    documented error cases must be handled by the calling entity
    (:ref:`ISO 26262-6:2018 8.4.5f <iso-trace-p6-c8-4-5-f>`).

* Pragmas

  * The entity must be contained within a pragma
    Unsuppress(All_Checks) region (so that language-defined checks
    disabled by ``-gnatp`` and/or ``-gnato0`` are re-enabled). The
    easiest way to ensure this is to issue the pragma immediately
    after the is keyword in the body.
  * If the entity uses a check suppression, i.e., a ``pragma
    Suppress``, ``pragma Suppress_All``, or ``pragma
    Assertion_Policy`` with the ``Ignore`` parameter, then do at least
    one of the following:

    * Assign a unique ID to the check suppression by using a
      structured comment as specified in the Traceability Model
      section so that tests can be traced to it in the :ref:`step-write-tests`
      step.
    * (Required for ASIL C and ASIL D units) Ensure the entity
      includes defensive checks to replace the disabled checks
      (:ref:`ISO 26262-6:2018, Table 1, row 1d
      <iso-trace-p6-c5-4-3-t1-1d>`).

For purposes of this verification, assume that all other subprograms
meet the above criteria. The verification described in this step is a
per-subprogram analysis, analogous to how GNATprove formally verifies
software on a per-subprogram basis.

Pass Criteria: As part of a global peer review, the reviewer(s)
confirmed that, for each entity with SPARK_Mode disabled or with
aspect ``Annotate => (GNATprove, Skip_Proof)`` or ``Annotate =>
(GNATprove, Skip_Flow_And_Proof)``, all the above properties are met.

Step ID: Review_Deactivated_SPARK

Distinction from Other Steps
''''''''''''''''''''''''''''

This step is separated from the other manual static verification steps
(such as :ref:`step-inspect-implementation`) for the following reasons:

* Process step atomicity: This step defines a set of review tasks
  specific to a particular area of concern. Merging this step with
  other code peer review steps would increase the risk that particular
  review steps might be missed, e.g., in developing the verification
  checklist for this process.

* Process steps: This step pairs with :ref:`step-static-analysis-unit` to perform
  static verification in lieu of the "SPARK Silver" / "SPARK Gold"
  verification that is done by GNATprove for ``SPARK_Mode => On``
  executable bodies without aspect ``Annotate => (GNATprove,
  Skip_Proof)`` or ``Annotate => (GNATprove, Skip_Flow_And_Proof)``.

* Testability: This step identifies manual verification activities for
  which no test cases ultimately need to be specified, because (1)
  most of the review tasks correspond to checks that will be
  automatically tested at runtime in the :ref:`step-verify-dynamic-assumptions`
  step (as long as check suppressions are avoided, as required above),
  and (2) the remaining review tasks (reviewing the justification,
  aliasing prohibitions, data flow contracts) are not suitable for
  verification through dynamic testing. It is helpful for the
  identification of test cases to separate out manual static
  verification tasks for which no evaluation of necessary test cases
  is required.

  * If check suppressions are used, then corresponding test cases must
    still be added to the Software Unit Verification Specification to
    provide evidence that these checks and assertions will not
    actually fail.

.. _step-manual-check-against-safety-manuals:

Manual Check Against Safety Manuals
"""""""""""""""""""""""""""""""""""

Review the following safety manuals and any known-problem lists
incorporated there by reference, and verify that all usage constraints
not checked by gnatkp are observed:

* Ada Compiler
* Ada Run-Time
* SPARK (GNATprove and sparklib)
* GNATcoverage
* GNATcheck

Step ID: Manual_Check_Against_Safety_Manuals

.. _step-inspect-implementation:

Inspect Implementation
""""""""""""""""""""""

As part of a local peer review, inspect (or otherwise review with
similar rigor) the unit implementation according to the Code
Inspection Worksheet in the Software Unit Verification Checklist
section to ensure that it satisfies all the non-formally-verified unit
requirements and non-formally-verified unit design fragments
(including, but not limited to, non-formal preconditions on called
subprograms, and non-formal postconditions on implemented executable
bodies).

Review all of the unit implementation to ensure all the following:

* Comprehensibility

  * The unit implementation is in-context-comprehensible to the
    reviewer. (Note: The unit implementation includes any pragmas used
    to suppress CodePeer diagnostics, as described in the
    :ref:`step-static-analysis-unit` step.)
  * The unit implementation observes the Ada/SPARK Guidelines (except
    for guidelines automatically enforced via GNATcheck rules).

* Correctness

  * The unit implementation contains no unintended functionality or
    unintended properties.
  * The unit implementation only withs package specifications that are
    within the scope of the unit (external packages of interface
    specifications provided/used by the software unit and internal
    packages of the unit itself).
  * Each non-formally-verified unit specification fragment imposed is
    fully satisfied by the combination of the traced downstream unit
    design fragments, the traced downstream unit requirements, and
    traced downstream implementation fragments.

Note: The Ada/SPARK Guidelines are applicable even if all unit
requirements and unit design fragments are formally-verified. However,
compliance with the Ada/SPARK Guidelines can be reviewed incrementally
over time, without any inspection of the entire unit ever needing to
be performed all at once.

Evidence of completion of the inspection must be recorded, along with
the outcome (whether the unit implementation is deemed sufficient to
satisfy the unit requirements and unit design fragments).

Note: ISO 26262 requires this verification to be done according to a
Verification Plan and Verification Specification. This process
partially defines the Verification Plan, the Verification
Specification, and what is expected in the Verification Report. This
process specifies where additional material must be developed in the
Software Unit Verification Plan and Software Unit Verification
Specification work products.

Step ID: Inspect_Implementation

Dynamic Verification
^^^^^^^^^^^^^^^^^^^^

.. _step-write-tests:

Write Tests
"""""""""""

Add test cases to the Software Unit Verification Specification that
can be executed to provide evidence that the software unit implements
the behaviors and properties specified in all the
non-formally-verified unit specification fragments.

Note: The non-formally-verified unit specification fragments consist
of:

* non-formally-verified unit requirements specified during the
  :ref:`step-capture-requirements` step or otherwise allocated to the software
  unit,

* non-formally-verified unit design constraints specified during the
  :ref:`step-capture-unit-design-constraints` step, and

* design documentation fragments developed during the
  :ref:`step-document-design-solutions` step.

For each non-formally-verified unit specification fragment, identify
the equivalence classes and boundary values evident in the fragment
and ensure the test cases in the Software Unit Verification
Specification cover all identified equivalence classes and boundary
values. In identifying equivalence classes and boundary values,
consider the Boolean expressions of expression functions referenced by
the fragment.

For traceability purposes, assign a unique ID to each test case. For
each test case in an ADS or ADB file, assign the unique ID using a
structured comment with the syntax specified in the Traceability Model
section, unless the name of a subprogram can serve as a
unique ID. (Note: The name of a subprogram cannot serve as a unique ID
if the subprogram is overloaded.)

Also use comments (e.g., the structured comment mentioned above) to
document the boundary values and equivalence classes covered by the
test case. This will support the evaluation of the sufficiency of the
test cases for each non-formally-verified unit specification fragment
in the :ref:`step-review-tests` step.

Create a trace link from each test case to each of the
non-formally-verified unit specification fragments that the test case
helps verify. Create trace links in the manner specified in the
Ada/SPARK Process Binding.

So that each instantiation of a generic package or subprogram can be
tested, test cases for generic packages and subprograms must
themselves be generic, with the same set of generic formal parameters
as the generic packages and subprograms they test. Also add test cases
that instantiate all the generic test cases (with any generic actual
parameters). These test cases will be used to evaluate the structural
coverage of the test cases, so that the completeness of the generic
test suite can be established once as part of verifying the software
unit instead of needing to be re-established for each generic
instantiation.

Also add test cases to the Software Unit Verification Specification
for instantiations of generics (even if the software unit is
implemented in Clean SPARK Platinum). For each instantiation of a
generic package or subprogram in the software unit design or
implementation:

* Identify the other software unit that implements the generic package
  or subprogram. (Note: This might be the same software unit.)
* Consult the other software unit's Software Unit Verification
  Specification.
* For each generic test case (if any) for the generic package or
  subprogram in the other Software Unit Verification Specification,
  create a test case that instantiates the generic test case with the
  same generic actual parameters as the generic actual parameters in
  the instantiation of the generic package or subprogram, and then
  executes the generic test case.
* If any part of the declaration or body of the generic package or
  subprogram uses a higher level of SPARK (considering the
  ``SPARK_Mode`` aspect and the ``Skip_Proof`` and
  ``Skip_Flow_And_Proof`` annotations) than the generic instantiation
  (even if the software unit is implemented in non-SPARK Ada), then
  add a ``SPARK_Mode => On`` non-proof-skipping test case that
  instantiates the generic package or subprogram with the same generic
  actual parameters as the generic actual parameters in the
  instantiation of the generic package or subprogram in the software
  unit, and record in the Software Unit Verification Specification
  that GNATprove must be invoked on the test case in the same manner
  as in the :ref:`step-verify-project` step. (This implies that the generic actual
  parameters must all be in SPARK.)

Also create a trace link from each diagnostic justification and each
uniquely-identified check suppression in the software unit design or
implementation to the test cases that provide evidence of the
soundness of those diagnostic justifications and check
suppressions. For example, trace each pragma Assume statement to test
cases that are used to verify that the assumption holds in practice.

Each unit test must yield an unambiguous PASS/FAIL result.

Step ID: Write_Tests

Tests Derived from Implementation
'''''''''''''''''''''''''''''''''

While developing software unit test cases for this step, do not use
the software unit implementation to determine the PASS/FAIL result of
each test case, except when instantiating generic test cases from
other software units (the expected behavior of the generic will
typically depend on the generic actual parameters in the
implementation of the instantiating unit). The software unit test
cases will contribute to the evaluation of structural coverage of the
software unit in the :ref:`step-unit-test-run-and-coverage` step, but structural
coverage is less effective at finding gaps in verification if the
criteria for determining software unit test PASS/FAIL results are
influenced by software unit implementation detail.

This implies that the software unit design should be sufficiently
complete to determine the PASS/FAIL result of each test case needed to
achieve the required structural coverage. Consequently, if structural
coverage gaps are identified in the :ref:`step-unit-test-run-and-coverage` step,
it is potentially necessary to revisit the Unit Design process steps
to add more detail to the software unit design. (The implied level of
detail varies based on the structural coverage metric, which must
match the Cleanliness-Adjusted ASIL as described in the
:ref:`step-unit-test-run-and-coverage` step.)

Test Cases Can Leverage Contracts
'''''''''''''''''''''''''''''''''

In the :ref:`step-verify-dynamic-assumptions` step, the software unit
implementation and test cases will be rebuilt with the ``-gnata`` and
``-gnatVa`` compiler switches. Per the `Debugging and Assertion
Control
<https://docs.adacore.com/R/docs/gnat-25.1/gnat_ugn/html/gnat_ugn/gnat_ugn/building_executable_programs_with_gnat.html#debugging-and-assertion-control>`_
section of [GUG]_, the ``-gnata`` compiler switch is equivalent to
``pragma Assertion_Policy (Check)``, which (among other things) causes
run-time checking of ``pragma Assume`` statements and most of the
contracts described in the :ref:`step-capture-requirements` step. The ``-gnatVa``
compiler switch causes run-time checking that data values are valid.

This implies that, except where ``pragma Assertion_Policy`` or
``pragma Validity_Checks`` is used to override the effect of these
switches, it is not necessary for test cases to check assumptions,
most contracts, and data validity. Test cases must cover the
equivalence classes and boundary values evident in the unit
specification fragments, and test cases must explicitly check for
compliance with non-formally-verified unit specification fragments
that are not expressed in the form of contracts, but the contracts
themselves are implicitly checked.

This is part of why the :ref:`step-capture-requirements` and
:ref:`step-capture-unit-design-constraints` steps ask to attempt to formalize
requirements and unit design constraints, even if it is known that the
unit specification fragments will not be formally-verified.

Testing of Expression Functions
'''''''''''''''''''''''''''''''

Testing of expression functions should be conducted in light of the
nature of expression functions in Ada. An Ada expression function is
effectively a formal definition of terminology that is sufficiently
precise that binary code can be automatically generated from it using
a safety-qualified toolchain. This section elaborates on the nature of
expression functions and the associated testing responsibilities.

If an expression function is in proven SPARK code and has no
non-formal requirements or design constraints, then the expression
function is by definition SPARK Platinum, even if it has no formal
requirements or design constraints either. Such an expression is
inherently formally-verified, so test cases do not need to be
developed to test that such an expression function behaves as
specified.

A non-SPARK-Platinum expression function only requires testing for two
purposes:

#. To ensure the completeness of the preconditions in its
   specification, given the Boolean expression. In non-proven SPARK
   code, missing preconditions may lead to incorrect or undefined
   behavior of the expression function.

#. To ensure the correctness of all other parts of its specification
   (i.e., other than the preconditions and Boolean expression), if
   any. While typically an expression function is specified entirely
   in terms of preconditions and the Boolean expression, it is
   permissible for the specification to be extended (e.g., with
   postconditions), and testing is required to ensure that the
   specification is consistent with the combination of the
   preconditions and the Boolean expression.

Note that a non-Ada-based software development process would typically
take the same approach as described above if it were possible to use a
safety-qualified toolchain to automatically generate source code from
a formal definition of terminology.

However, where an expression function (even a public expression
function) is called from other code, it can introduce additional
equivalence classes and boundary values that can require additional
testing of the caller.

.. _step-review-tests:

Review Tests
""""""""""""

Review tests with a local peer review. The local peer reviewer must
verify that:

* Each non-formally-verified unit specification fragment traces to
  test cases that collectively verify all the properties and behaviors
  in the unit specification fragment and collectively cover all the
  boundary values and equivalence classes evident in the unit
  specification fragment.

* Each diagnostic justification and each uniquely-identified check
  suppression traces to test cases that collectively verify the
  correctness of the diagnostic justification or check suppression.

* Each test case traces to one unit specification fragment it
  supports, unless the test case is merely an instantiation of a
  generic test case.

* Test cases for generic packages and subprograms comply with the
  corresponding rules in the :ref:`step-write-tests` step.

* Generic instantiations are tested per the corresponding rules in the
  :ref:`step-write-tests` step.

Pass Criteria: A local peer reviewer confirmed all of the above.

Step ID: Review_Tests

.. _step-formally-verify-test-cases:

Formally Verify Test Cases
""""""""""""""""""""""""""

If the Software Unit Verification Specification specifies that
GNATprove must be used to formally verify test cases (i.e., test cases
that instantiate formally-verified generics), then invoke GNATprove:

.. code-block:: bash

   gnatprove -P my_test_project --clean
   gnatprove -P my_test_project -U additional_switches

where my_test_project is the name of the project containing the test
cases requiring proof and additional_switches consists of zero or more
additional GNATprove switches.

The GNATprove switches specified in my_test_project and the GNATprove
switches specified on the second gnatprove command line must
collectively comply with the Requirements Concerning GNATprove
Switches section.

Record the precise commands executed, their console output, and their
exit statuses in the Software Unit Verification Report.

Pass Criteria: GNATprove reports no warnings, errors, or
low/medium/high check messages. (Alternatively, you can just check
that gnatprove exited with a zero exqit status.)

Step ID: Formally_Verify_Test_Cases

.. _step-unit-test-run-and-coverage:

Unit Test Run And Coverage
""""""""""""""""""""""""""

The unit tests developed in the :ref:`step-write-tests` step must be executed in
accordance with the Software Unit Verification Specification, and
results must be evaluated in accordance with :ref:`ISO 26262:2018 Part
8 9.4.3.3 <iso-trace-p8-c9-4-3-3>` and :ref:`9.4.3.4
<iso-trace-p8-c9-4-3-4>`.

If the cleanliness-adjusted ASIL of the unit is QM, then run the
previously-developed tests, record the test results in the Software
Unit Verification Report, confirm that all the tests passed, and skip
the rest of this step.

Otherwise, proceed with the rest of this step.

Build the coverage runtime corresponding to the unit test execution
environment. Note: The development of the coverage runtime for an
execution environment not supported by AdaCore is out of the scope of
this process.

First, install the coverage runtime into your project:

.. code-block:: bash

   gnatcov setup --prefix=my_coverage_runtime

where my_coverage_runtime is the destination directory into which to
install the coverage runtime. See [GDM]_ section `Setting up the
coverage runtime library
<https://docs.adacore.com/R/docs/gnat-25.1/gnatdas/html/gnatdas_ug/gnatcov/src_traces.html#setting-up-the-coverage-runtime-library>`_
for more information about setting up the coverage runtime library.

Create the instrumented fork of the project:

.. code-block:: bash

   gnatcov instrument --level=my_coverage_level -P my_unit_project \
     --dump-channel=my_dump_channel \
     --dump-trigger=my_dump_trigger \
     --runtime-project=my_coverage_runtime

where my_coverage_level is either ``stmt``, ``stmt+decision``, or
``stmt+mcdc`` as appropriate for the cleanliness-adjusted ASIL of the
software unit (statement coverage for ASIL A, statement and decision
coverage for ASILs B and C, and statement and MC/DC coverage for ASIL
D), and where my_dump_trigger and my_dump_channel are appropriate for
the unit test execution environment, and my_coverage_runtime is the
directory previously passed to gnatcov setup. See [GDM]_ section
`Producing source traces with gnatcov instrument
<https://docs.adacore.com/R/docs/gnat-25.1/gnatdas/html/gnatdas_ug/gnatcov/src_traces.html#>`_
for more information, including about how to pick a dump trigger and
dump channel appropriate to your test environment.

Note: For an ordinary executable with a main subprogram in Ada or C
you should be able to use the ``atexit`` dump trigger and ``bin-file``
dump channel with the bundled default coverage runtime. If you use the
manual dump trigger, then see the GNATcoverage documentation for how
to trigger the coverage dump.

Note: Where MCDC is required, this process specifies the use of
Masking MCDC (selected with ``--level=stmt+mcdc``), not the more
strict interpretations of MCDC that are also supported by
GNATcoverage. This is consistent with the recommendations in
DOT/FAA/AR-01/18 ("An Investigation of Three Forms of the Modified
Condition Decision Coverage (MCDC) Criterion").

Build the project with instrumented coverage:

.. code-block:: bash

   gprbuild -P my_unit_project \
     --src-subdirs=gnatcov-instr \
     --implicit-with=my_coverage_runtime/share/gpr/gnatcov_rts.gpr \
     -cargs:Ada \
     -gnatec=installation_directory/share/examples/gnatcoverage/support/instrument-spark.adc

where my_coverage_runtime is the directory previously passed to
gnatcov setup and installation_directory is the location of your GNAT
Dynamic Analysis Suite (DAS) installation (used to find the directory
containing the instrument-spark.adc file). Note that such instrumented
builds are not meant for proof or shipping; they are only for
gathering test coverage data. See [GDM]_ section `Building
instrumented components
<https://docs.adacore.com/R/docs/gnat-25.1/gnatdas/html/gnatdas_ug/gnatcov/src_traces.html#building-instrumented-components>`_
for more information about doing the coverage-enabled build.

Then execute the unit tests, record the test results in the Software
Unit Verification Report, and confirm that all the unit tests passed.

The execution will produce a trace in a coverage-runtime-specific
manner. Decode the traces:

.. code-block:: bash

   gnatcov coverage --level=my_level -P my_unit_project \
     my_trace_files --annotate=xcov+

where my_trace_files is the list of paths of the files that contain
the trace data. See [GDM]_ section `Source coverage analysis with
gnatcov coverage
<https://docs.adacore.com/R/docs/gnat-25.1/gnatdas/html/gnatdas_ug/gnatcov/cov_source.html>`_
for more information about analyzing the coverage trace files.

Finally, for each of the generated .xcov files, review the coverage
gaps and identify the coverage deviations (gaps).

Record the precise gprbuild and gnatcov commands executed, their
console output, their exit statuses, and the contents of the .xcov
files in the Software Unit Verification Report. (Note: .xcov file
contents can be incorporated by reference.)

Pass Criteria: All tests were run and passed, and if the
cleanliness-adjusted ASIL of the unit is not QM, coverage was
collected during the execution of the tests using the structural
coverage metric corresponding to the cleanliness-adjusted ASIL of the
unit.

Step ID: Unit_Test_Run_And_Coverage

Use of Cleanliness-Adjusted ASILs In This Step
''''''''''''''''''''''''''''''''''''''''''''''

The level of structural coverage required is determined by the
cleanliness-adjusted ASIL of the unit, not the ASIL to which the unit
is developed. This implies:

* If the cleanliness-adjusted ASIL of the unit is QM, then no
  structural coverage is required, even if the unit is developed to
  ASIL A, B, C, or D.

* If the cleanliness-adjusted ASIL of the unit is ASIL A, then only
  statement coverage is required, even if the unit is developed to
  ASIL B, C, or D.

* If the cleanliness-adjusted ASIL of the unit is ASIL B or ASIL C,
  then only statement and decision coverage are required, even if the
  unit is developed to ASIL D.

By definition, if the cleanliness-adjusted ASIL of the unit is X but
the unit is developed to ASIL Y where Y > X, then the unit is
implemented in clean SPARK and all of its requirements above ASIL X
are formally-verified. While the reduction in structural coverage
obligations could mask a systematic fault, the risk that such a
systematic fault will lead to the violation of an ASIL Z requirement
allocated to the unit, for some Z such that X < Z <= Y, is adequately
controlled by the use of GNATprove in the :ref:`step-verify-project` step, and the
risk that such a systematic fault will lead to the violation of an
ASIL Z requirement outside the unit is already captured in the unit
requirements and their respective ASILs. (Safety analysis and DFA must
consider ASILs of specific safety requirements allocated to the
software unit, not just the ASIL to which the software unit is
developed, because those analyses would not necessarily be re-executed
if the software unit were subsequently re-implemented as a multi-unit
software component that allocates the QM / lower-ASIL safety
requirements to a QM / lower-ASIL unit.)

Note: The use of cleanliness-adjusted ASILs to determine structural
coverage requirements does not constitute a deviation from
ISO 26262. In :ref:`ISO 26262-6:2018, Table 9 <iso-trace-p6-c9-4-4>`,
the statement coverage, branch coverage, and MC/DC structural coverage
metrics are recommendations (sometimes high recommendations), not
strict requirements. This process presents GNATprove coverage as an
alternative means of evaluating the completeness of verification. When
clean SPARK is used, GNATprove provides 100% coverage of formal
requirements, obviating the need to collect structural coverage
through testing.

.. _step-handle-coverage-deviations:

Handle Coverage Deviations
""""""""""""""""""""""""""

For each coverage deviation (every statement, decision, or condition
gap identified in the :ref:`step-unit-test-run-and-coverage` step), handle it by
selecting one of the options from the following list, preferring
earlier options over later options:

* Justify it by the fact that the statement, decision, or condition is
  part of a fully formally-verified subprogram, i.e., all the unit
  requirements or unit design constraints applicable to the subprogram
  are formally specified and the subprogram has ``SPARK_Mode`` On. In
  this case, the objectives of structural coverage as defined in
  :ref:`ISO 26262-6:2018, 9.4.4 <iso-trace-p6-c9-4-4>` have already
  been achieved for the particular subprogram and there is no need to
  analyze the structural coverage of the subprogram.

* Justify it by the fact that the statement, decision, or condition is
  strictly necessary for GNATprove to be able to prove compliance with
  a type constraint (a range constraint or a null exclusion), an
  expression-based contract (a type predicate, a precondition of a
  called subprogram, or a postcondition of the incompletely-covered
  executable body), or an assertion pragma (``pragma Assert``,
  ``pragma Loop_Invariant``, or ``pragma Loop_Variant``).

  * Note: This process does not require each type constraint,
    expression-based contract, or assertion pragma to be justified
    with coverage of its own. Per :ref:`ISO 26262-6:2018, Table 7
    <iso-trace-p6-c9-4-2-t7-1j>`, ISO 26262 permits unit tests to be
    derived from "requirements", which are defined to include the unit
    design specification. This process considers type constraints,
    expression-based contracts, and assertion pragmas to be part of
    the unit design specification for purposes of structural coverage
    evaluation.

* Identify an aspect of the unit requirements or unit design for which
  a testing gap was exposed by the coverage deviation, and improve the
  testing of that aspect of the unit requirement or unit design.

  * Note: Unit tests should never be developed for the sole purpose of
    addressing coverage deviations. Unit tests must always be based on
    the requirements and design.

* Remove unintended code.

* Add more detail to the unit design, and use the new unit design
  detail to develop additional test cases.

* (For cleanliness-adjusted ASIL C and below only) Justify uncovered
  code, e.g., by explaining that the code does not execute in any
  situation in which it could have safety impact.

  * Note: This process does not permit coverage gaps to be justified
    by such means in cleanliness-adjusted ASIL D software units,
    because fault injection test is highly recommended for ASIL D
    software units by :ref:`ISO 26262-6:2018, Table 7, row 1l
    <iso-trace-p6-c9-4-2-t7-1l>`, and fault injection test is a means
    of closing all coverage gaps. Fault injection test involves
    modifying the software unit for purposes of testing corner cases
    of the software unit that would otherwise be unreachable through
    dynamic testing.

Pass Criteria: Each remaining coverage deviation justified per the
above.

Step ID: Handle_Coverage_Deviations

.. _step-verify-dynamic-assumptions:

Verify Dynamic Assumptions
""""""""""""""""""""""""""

Recompile and run unit tests with the project file modified as follows:

* Ensure that the ``-gnata`` and ``-gnatVa`` compiler switches are
  present in Default_Switches ("Ada") in the ``Compiler`` package

* Ensure that the ``-gnatp`` and ``-gnato0`` compiler switches are not
  present in ``Default_Switches ("Ada")`` in the ``Compiler`` package

* Ensure that the file specified by ``Global_Configuration_Pragmas``
  in the ``Builder`` package includes ``pragma Initialize_Scalars``

These modifications help ensure that in the presence of software units
that mix Ada with SPARK, all assumptions hold at the unit-internal
boundaries between Ada and SPARK.

Pass Criteria: All tests were run and passed, without any exceptions
being raised during test execution.

Step ID: Verify_Dynamic_Assumptions

Compiler Switches Outside This Step
'''''''''''''''''''''''''''''''''''

Outside this step and the :ref:`step-run-integration-tests` step, this process
prohibits the use of ``-gnata`` and does not require the use of
``-gnatVa``. These options enable potentially-expensive checks that
are not crucial for software that has been verified, whether formally
or non-formally.

Outside this step and the :ref:`step-run-integration-tests` step, this process
permits the use of ``-gnatp`` and ``-gnato0`` to suppress
language-defined checks when compiling executable bodies with
``SPARK_Mode => On`` and without aspects ``Annotate => (GNATprove,
Skip_Proof)`` or ``Annotate => (GNATprove,
Skip_Flow_And_Proof)``. Language-defined checks are not needed for
such SPARK code because GNATprove formally verifies that such SPARK
code will never fail a language-defined check, assuming code outside
of SPARK complies with all the requirements. However, for executable
bodies with ``SPARK_Mode => Off`` or with aspects ``Annotate =>
(GNATprove, Skip_Proof)`` or ``Annotate => (GNATprove,
Skip_Flow_And_Proof)``, this process requires the use of ``pragma
Unsuppress (All_Checks)`` to undo the effects of ``-gnatp`` and
``-gnato0`` on that code, as these control relatively inexpensive
checks that are valuable in controlling the effects of stray memory
writes.

Memory Resource Utilization
'''''''''''''''''''''''''''

The use of ``-gnata`` and ``pragma Initialize_Scalars`` can
significantly increase the amount of primary stack space, secondary
stack space, and heap memory required to execute the software
unit. For example, a subprogram that does not call any subprograms in
its body may still call subprograms in its contracts. During this
step, it might be necessary to temporarily increase stack and heap
sizes above the values used in production.

Check Suppressions
''''''''''''''''''

This process permits the use of check suppressions (see Terminology
section), but check suppressions in non-proven code must be coupled
with either comparable defensive checks or comparable test cases.

.. _step-develop-verification-report:

Develop Verification Report
^^^^^^^^^^^^^^^^^^^^^^^^^^^

You have already added various verification evidence to the Software
Unit Verification Report during the following steps:

* :ref:`step-inspect-unit-design`: Evidence of local peer review per the
  Verification Checklist for Software Unit Design.
* :ref:`step-compile-project`: The precise gprbuild command executed, its console
  output, and its exit status.
* :ref:`step-verify-project`: The precise gnatprove commands executed, their
  respective console output, and their exit statuses.
* :ref:`step-automated-check-against-coding-std`: The precise gnatcheck and gnatkp
  commands executed, their respective console output, and their exit
  statuses.
* :ref:`step-static-analysis-unit`: The precise CodePeer command executed, its
  console output, its exit status, and the contents of the output
  files.
* :ref:`step-check-stack-usage-unit`: The precise gnatstack command executed, its
  console output, its exit status, and the contents of the output
  files.
* :ref:`step-formally-verify-test-cases`: The precise gnatprove commands executed,
  their respective console output, and their exit statuses.
* :ref:`step-unit-test-run-and-coverage`: Test results and, if applicable, the
  precise gprbuild and gnatcov commands executed, their respective
  console output, their exit statuses, and the contents of the .xcov
  files.

In this step, complete the Software Unit Verification Report by adding:

* A reference to the Software Unit Verification Plan.
* A reference to the Software Unit Verification Specification.
* The specific versions of the files containing the software unit
  design and implementation that were verified. Where possible, you
  should use Configuration Management features to minimize manual
  effort.
* Evidence of completion of the Verification Checklists for Software
  Unit Implementation and Verification, and which peer reviewer(s)
  completed it.
* An unambiguous statement of whether unit verification passed or
  failed.

  * Note: This process constrains the Verification Plan in mandating
    that verification fails unless all checklist questions are
    answered with an unequivocal "yes".

Step ID: Develop_Verification_Report
