.. Copyright (C) 2024 - 2025 NVIDIA CORPORATION & AFFILIATES
.. Copyright (C) 2021 - 2024 AdaCore
..
.. Permission is granted to copy, distribute and/or modify this document
.. under the terms of the GNU Free Documentation License, Version 1.3 or
.. any later version published by the Free Software Foundation; with the
.. Invariant Sections being "Attribution", with no Front-Cover
.. Texts, and no Back-Cover Texts.  A copy of the license is included in
.. the section entitled "GNU Free Documentation License".

.. _sec-usage-analysis:

============================
Software Tool Usage Analysis
============================

This section identifies each of the tools prescribed by the process
steps specified in this document, analyzes each tool to determine the
Tool Impact (TI) and Tool error Detection (TD), and classifies each
tool at the corresponding Tool Confidence Level (TCL), per ISO
26262-8:2018, 11.4.5.

For each tool:

* The usage of the tool in this process is documented in accordance
  with 8-11.4.5.1:

  * The intended purpose is documented in accordance with 8-11.4.5.1a.

  * The inputs and outputs are documented in accordance with 8-11.4.5.1b.

    * Except where stated otherwise, all tools in this section consume
      the same inputs: GPR, ADC, ADS, and ADB files.

  * The usage procedures and constraints are documented in accordance
    with 8-11.4.5.1c.

    * Except where specified otherwise, the process steps themselves
      document this information.

  * The usage of the tool in this process is analyzed in accordance
    with 8-11.4.5.2:

    * The Tool Impact (TI) class is determined per 8-11.4.5.2a.
    * The Tool error Detection (TD) class is determined per 8-11.4.5.2b.
    * Where the TI and TD are estimated, they are estimated
      conservatively as recommended by 8-11.4.5.3.

  * The minimum Tool Confidence Level (TCL) of the tool required for
    this process is determined in accordance with 8-11.4.5.4.

    * Note that there may be other use cases for the tools outside
      this process that in some cases necessitate higher TCLs. Such
      concerns are outside the scope of this process.

GPRbuild
--------

GPRbuild is used in the following process steps:

* :ref:`step-verify-formal-requirement-consistency`
* :ref:`step-compile-project`
* :ref:`step-unit-test-run-and-coverage`

The usage of GPRbuild:

* The intended purpose of GPRbuild varies by process step:

  * :ref:`step-verify-formal-requirement-consistency`: To verify the consistency
    of the formally-specified portions of the unit requirements. (This
    is also accomplished by :ref:`step-compile-project`.)

  * :ref:`step-compile-project`: To verify the consistency of all the ADS and ADB
    files in the project and to compile the ADB files into object
    code.

  * :ref:`step-unit-test-run-and-coverage`: To compile the unit test
    implementations into object code.

* Regarding the GPRbuild inputs:

  * For the :ref:`step-verify-formal-requirement-consistency` step, the ADS/ADB
    inputs are exclusively ADS files that make up the software
    interfaces.

  * For the :ref:`step-compile-project` step, the ADS/ADB inputs include the ADS
    and ADB files that make up the software interfaces, the unit
    design, and the unit implementation.

  * For the :ref:`step-unit-test-run-and-coverage` step, the ADS/ADB inputs are
    the ADS and ADB files that make up the unit test cases.

* The GPRbuild outputs are:

  * Potential errors and/or warnings detected attempting to compile
    the inputs

  * Object files (``*.o``) and associated Ada Library Information iles
    (``*.ali``), if no errors or warnings are generated

Analysis of the usage of GPRbuild:

* **TI2** is selected because a bug in GPRbuild that manifests while
  executing the :ref:`step-compile-project` step could introduce a systematic
  fault in the deployed object code.

* **TD3** is selected because, where GNATprove is used in lieu of unit
  testing, we have a low degree of confidence that a malfunction of
  GPRbuild will be prevented or detected.

Based on the above, GPRbuild is classified at **TCL3**.

GNATprove
---------

GNATprove is used in the following process steps:

* :ref:`step-verify-formal-requirement-consistency`
* :ref:`step-verify-unit-design`
* :ref:`step-implement-spark-package`
* :ref:`step-verify-project`

The usage of GNATprove:

* The intended purpose of GNATprove varies by process step:

  * :ref:`step-verify-formal-requirement-consistency`: To verify the consistency
    of the formally-specified unit requirements. (This is also
    accomplished by :ref:`step-verify-unit-design` and :ref:`step-verify-project`.)

  * :ref:`step-verify-unit-design`: To verify the consistency of the
    formally-specified fragments of the unit design with one another
    and with the formally-specified unit requirements.  (This is also
    accomplished by :ref:`step-verify-project`.)

  * :ref:`step-implement-spark-package`: To incrementally verify the subprograms
    of the unit. (This is also accomplished by :ref:`step-verify-project`.)

  * :ref:`step-verify-project`: To verify the consistency of all SPARK content in
    the ADS and ADB files and to verify all SPARK implementations
    fulfill all their contracts.

* Regarding the GNATprove inputs:

  * For the :ref:`step-verify-formal-requirement-consistency` step, the ADS/ADB
    inputs are exclusively ADS files that make up the software
    interfaces.

  * For the :ref:`step-verify-unit-design` step, the ADS/ADB inputs include the
    ADS and ADB files that make up the software interfaces and the
    unit design.

  * For the :ref:`step-implement-spark-package` and :ref:`step-verify-project` steps, the
    ADS/ADB inputs include the ADS and ADB files that make up the
    software interfaces, the unit design, and the unit implementation.

* The GNATprove outputs are:

  * Potential errors and/or warnings detected attempting to verify the
    inputs

  * Potential check messages for issues detected attempting to verify
    the inputs

Analysis of the usage of GNATprove:

* **TI2** is selected because a bug in GNATprove that manifests while
  executing the :ref:`step-verify-project` step could result in a failure to
  detect systematic faults in the unit design or unit implementation.

* **TD3** is selected because, where GNATprove is used in lieu of unit
  testing, we have a low degree of confidence that a malfunction of
  GNATprove will be prevented or detected.

Additional notes:

* GNATprove must be qualified to be free of false negatives, subject
  to GNATprove assumptions. Being free of false negatives implies the
  following properties:

  * Check messages and/or error messages are issued unless each
    ``SPARK_Mode => On`` non-``Skip_Flow``/``Skip_Flow_And_Proof``
    subprogram body in the scope of the project file (passed on the
    command line with the ``-P`` command line option to ``gnatprove``)
    is free of non-storage run-time errors and satisfies all its
    contracts, assuming all documented GNATprove assumptions are
    satisfied.

  * Warning messages are issued for all warning conditions documented
    as "guaranteed" to issue warnings.

  * The gnatprove process exit status is non-zero if any error message
    is issued.

  * If ``--checks-as-errors`` is passed on the gnatprove command line,
    then the gnatprove process exit status is non-zero if any check is
    issued.

  * If ``--warnings=error`` is passed on the gnatprove command line,
    then the gnatprove process exit status is non-zero if any warning
    is issued.

Based on the above, GNATprove is classified at **TCL3**.

GNATstack
---------

GNATstack is used exclusively in the :ref:`step-check-stack-usage-unit` step.

The usage of GNATstack:

* The intended purpose of GNATstack is to detect subprograms and call
  chains that use more than expected amounts of stack space.

* The output of GNATstack is the amount of stack space needed by each
  subprogram, along with an identification of any potential weaknesses
  in the analysis that require supplementation with manual analysis.

Analysis of the usage of GNATstack:

* **TI2** is selected because a stack overflow could lead to the
  violation of a safety requirement for availability. (Absent stack
  guards, a stack overflow could also lead to data corruption.)

* **TD2** is selected because besides using GNATstack, integration
  testing also gives some confidence, but not absolute confidence,
  that stack sizes will be sufficient in practice for units subject to
  this process. (In general, sufficient stack allocation is a system
  integration question, and unit-level measures alone cannot account
  for such faults.)

Based on the above, GNATstack is classified at **TCL2**.

GNATstub
--------

GNATstub is used exclusively in the :ref:`step-create-adb` process step.

The usage of GNATstub:

* The intended purpose of GNATstub is to ease the creation of ADB
  files by automatically generating some of the content.

* The GNATstub inputs are ADS files.

* The GNATstub outputs are ADB files containing stub implementations
  of the subprograms declared in the ADS files.

Analysis of the usage of GNATstub:

* **TI2** is selected because a bug in GNATstub that manifests as an
  incorrect ADB file could conceivably yield an ADB file with a
  systematic fault in it.

* **TD1** is selected because the Unit Verification process is
  sufficient to address the risk of unit implementation errors,
  whether those errors exist in code that was manually developed or
  automatically generated, and the Unit Verification process is
  applied in the same way regardless of the origin of the ADB file
  content.

Based on the above, GNATstub is for purposes of this process
classified at **TCL1**.

GNATcheck and GNATkp
--------------------

Note: GNATcheck / GNATkp are grouped together because they are
logically one tool.

GNATcheck / GNATkp are used only in the following process steps:

* :ref:`step-automated-check-against-coding-std`
* :ref:`step-fix-coding-std-issues`

The usage of GNATcheck / GNATkp:

* The intended purpose of GNATcheck / GNATkp is to detect the
  following:

  * Code patterns that may be difficult to understand

  * Code patterns that violate restrictions in the safety manuals of
    other qualified tools

* The GNATcheck / GNATkp outputs are potential errors and/or warnings
  concerning issues detected in the code.

Analysis of the usage of GNATcheck / GNATkp:

* **TI2** is selected because a bug in GNATcheck / GNATkp could result
  in a GPRbuild/GNATprove safety manual violation going undetected,
  leading to erroneous code generation or incomplete verification.

* **TD3** is selected because this process relies exclusively on
  GNATcheck/GNATkp to enforce some safety manual restrictions.

Based on the above, GNATcheck / GNATkp is classified at **TCL3**.

GNATcoverage
------------

GNATcoverage is used exclusively in the :ref:`step-unit-test-run-and-coverage`
process step.

The usage of GNATcoverage:

* The intended purpose of GNATcoverage is to evaluate the completeness
  of dynamic verification through measurement and reporting of
  structural coverage gaps.

* The GNATcoverage inputs include, in addition to the project, a
  coverage level (statement coverage, decision coverage, or MC/DC).

* The GNATcoverage output is a coverage report indicating what
  structural coverage gaps were found during unit testing.

Analysis of the usage of GNATcoverage:

* **TI2** is selected because a bug in GNATcoverage could, in
  conjunction with a code inspection error, a unit test gap, and a
  systematic fault, result in that systematic fault not being detected
  during development.

* **TD3** is selected because in the authors' experience it is common
  that unit tests generated based on the unit design have gaps that
  are identified through analysis of structural coverage.

Based on the above, GNATcoverage is classified at **TCL3**.

CodePeer
--------

CodePeer is used exclusively in the :ref:`step-static-analysis-unit` and
:ref:`step-static-analysis-integration` steps.

The usage of CodePeer:

* The intended purpose of CodePeer is to identify non-proven Ada code
  that could potentially violate Ada language rules. (This is not
  necessary for proven SPARK code because GNATprove formally verifies
  that proven SPARK code complies with Ada language rules.)

* The CodePeer output is a report of all Ada code sequences identified
  as potentially violating Ada language rules in non-proven code.

Analysis of the usage of CodePeer:

* **TI2** is selected because a bug in CodePeer could, in conjunction
  with a systematic fault, a code inspection error, and a unit test
  gap, lead to a systematic fault not being detected during
  development.

* **TD1** is selected because the manual inspection processes
  necessarily must analyze all potential violations of the Ada
  language rules, because CodePeer offers no soundness guarantee.

Based on the above, CodePeer is classified at **TCL1**.
