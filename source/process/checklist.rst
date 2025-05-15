.. Copyright (C) 2024 - 2025 NVIDIA CORPORATION & AFFILIATES
.. Copyright (C) 2021 - 2024 AdaCore
..
.. Permission is granted to copy, distribute and/or modify this document
.. under the terms of the GNU Free Documentation License, Version 1.3 or
.. any later version published by the Free Software Foundation; with the
.. Invariant Sections being "Attribution", with no Front-Cover
.. Texts, and no Back-Cover Texts.  A copy of the license is included in
.. the section entitled "GNU Free Documentation License".

.. _sec-checklist:

=====================================
Software Unit Verification Checklists
=====================================

This section provides two verification checklists that are to be used
to provide evidence of correct execution of this process for each
software unit. The two verification checklists are:

.. contents:: Checklists and worksheets
   :backlinks: none


The Verification Checklist for Software Unit Requirements is expected
to be incorporated (e.g., by reference) into the corresponding
Verification Specification for those software unit requirements (see
ISO 26262-6:2018, 6.4.7). The development of that Verification
Specification is out of the scope of this process. This process only
covers software requirements specification at all because this process
introduces the practice of incorporating software unit requirements
into the public parts of external ADS files for purposes of enabling
formal specification and verification of software unit requirements.

Note: An organization may consider the software unit requirements to
be part of the software architectural design, in which case the
software architectural design Verification Specification would be the
particular Verification Specification that would need to incorporate
the Verification Checklist for Software Unit Requirements.

The Verification Checklist for Software Unit Design and Implementation
is expected to be incorporated by reference into the Software Unit
Verification Specification work product described in this process.

Note: Each checklist question must be usable by:

* reviewers on the software unit development team,
* confirmation reviewers, and
* assessors.

Separate checklists are not provided for each of these stakeholders
because the same checklist questions apply to all three of these
roles. Where expectations are different for the different roles, the
checklist row calls out the specific differences in the roles in
answering the checklist question.

If multiple reviewers are completing checklists for the same software
interface or software unit, reviewers cannot share a checklist among
one another; each review must complete a checklist separately. Except
where specified otherwise, any non-zero number of reviewers is
sufficient as long as no fragment of the software interface or
software unit was authored by all the reviewers (every fragment must
have at least one reviewer who is not the author, as is required by
local peer reviews).

It is the intent of this process that confirmation reviewers and
assessors use the same checklist as reviewers. Other checklists that
were not developed with formal verification in mind are likely to
underemphasize areas that are of primary concern where formal
verification is used and are likely to overemphasize areas that are of
lesser concern where formal verification is used.

Checklist items are color-coded according to what situations they
apply to:

.. role:: cl_all

* Checklist items with a :cl_all:`light-green` background apply to every
  software interface and software unit developed according to this
  process.

.. role:: cl_not_platinum

* Checklist items with a :cl_not_platinum:`light-blue` background
  apply to every software interface and software unit developed
  according to this process except for SPARK Platinum software
  interfaces and clean SPARK Platinum software units (see the
  Terminology section).

.. role:: cl_ada

* Checklist items with a :cl_ada:`light-red` background apply to any
  software unit developed according to this process that does not
  enable SPARK_Mode throughout the entirety of the unit or that skips
  proof for part or all of the unit.

.. role:: cl_automated

* Checklist rows with a :cl_automated:`gray` background identify
  activities for which no manual verification of compliance is needed.

Checklist item numbers are suffixed with either (A) indicating that it
is expected to be automatable through other processes and tools or (M)
indicating that manual verification is inherently required.

In order to complete these checklists, the reviewer needs access to:

* The software unit requirements.
* The software unit files (e.g., GPR, ADC, ADS, and ADB files).
* The precise commands executed per this process and the corresponding
  console output, exit statuses, and output file contents recorded in
  the Software Unit Verification Report.

Verification Checklist for Software Unit Requirements
-----------------------------------------------------

The Verification Checklist for Software Unit Requirements consists of
the following parts:

* Per-software-unit checklist
* Per-software-interface checklist

Per-Software-Unit Checklist
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Complete this once per Ada software unit.

.. include:: checklist/per-software-unit.rst

Per-Software-Interface Checklist
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Every software interface identified in checklist question 1 in the
per-software-unit checklist must be covered by exactly one of the
following per-software-interface checklists. It is acceptable to cover
multiple software interfaces with the same per-software-interface
checklist as long as each person completing the checklist gives full
consideration to all the software interfaces within the scope of the
checklist.

Checklist question 1 in this checklist asks for what software
interfaces are covered by the particular checklist. Every subsequent
question in this checklist must only be answered "Yes" if the answer
is "Yes" for each and every software interface identified in the
answer to checklist question 1.

.. include:: checklist/per-software-interface.rst

Verification Checklists for Software Unit Design and Implementation
-------------------------------------------------------------------

Complete each of the checklists in this section once per Ada software
unit developed according to this process.

Verification Checklist for Software Unit Design
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Complete this once per Ada software unit.

.. include:: checklist/software-unit-design.rst

Verification Checklist for Software Unit Implementation and Verification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Complete this once per Ada software unit.

.. include:: checklist/software-unit-implementation.rst

Diagnostic Justifications Verification Worksheet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Complete this worksheet if required by the Verification Checklist for
Software Unit Implementation and Verification.

This worksheet includes checklist questions related to:

* Non-formally-verified assumptions (a.k.a. GNATprove indirect
  justifications):

  * .. code-block:: ada

       pragma Assume (condition, justification);

* GNATprove warning suppressions:

  * .. code-block:: ada

       pragma Warnings (GNATprove, Off, warning,
                        Reason => justification);
       ...
       pragma Warnings (GNATprove, On, warning);

  * .. code-block:: ada

       pragma Warnings (Off, warning, Reason => justification);
       ...
       pragma Warnings (On, warning);

* GNATprove direct justifications (a.k.a. GNATprove check message
  direct justifications):

  * .. code-block:: ada

       pragma Annotate (GNATprove, False_Positive,
                        check_message,
			justification);

  * .. code-block:: ada

       pragma Annotate (GNATprove, Intentional,
                        check_message,
			justification);

* GNATcheck rule exemptions:

  * .. code-block:: ada

       pragma Annotate (GNATcheck, Exempt_On,
                        rule_name,
			justification);
       ...
       pragma Annotate (GNATcheck, Exempt_Off, rule_name);

.. include:: checklist/ws-justifications.rst

Non-Proven Ada Worksheet
^^^^^^^^^^^^^^^^^^^^^^^^

Complete this worksheet if required by the Verification Checklist for
Software Unit Implementation and Verification.

In completing this worksheet, consider all non-proven code, and only
answer "yes" to a checklist question if the answer is "yes" for all
the non-proven code:

* Code with no explicit ``SPARK_Mode`` aspect or pragma
* Code for which the innermost relevant ``SPARK_Mode`` aspect or
  pragma set ``SPARK_Mode`` to ``Off``
* Code with the ``Annotate => (GNATprove, Skip_Proof)`` aspect
* Code with the ``Annotate => (GNATprove, Skip_Flow_And_Proof)``
  aspect

.. include:: checklist/ws-nonspark.rst

Code Inspection Worksheet
^^^^^^^^^^^^^^^^^^^^^^^^^

Complete the code inspection worksheet once per unit. Here, the "code"
of a software unit includes all the contents of the ADS/ADB files,
including software unit design.

.. include:: checklist/ws-code-inspection.rst
