.. Copyright (C) 2024 - 2025 NVIDIA CORPORATION & AFFILIATES
.. Copyright (C) 2021 - 2024 AdaCore
..
.. Permission is granted to copy, distribute and/or modify this document
.. under the terms of the GNU Free Documentation License, Version 1.3 or
.. any later version published by the Free Software Foundation; with the
.. Invariant Sections being "Attribution", with no Front-Cover
.. Texts, and no Back-Cover Texts.  A copy of the license is included in
.. the section entitled "GNU Free Documentation License".

.. _sec-process-assumptions:

=============================
Prerequisites and Assumptions
=============================

General Assumptions
-------------------

This process assumes that:

* There is a software architectural design.

  * This process does not restrict the tools used to specify the
    software architectural design.
  * However, it is strongly recommended that the software
    architectural design not include software unit design or
    implementation work products.

    * (But documenting architectural design in header files and ADS
      files is typically a reasonable approach, especially in
      combination with tools such as Doxygen and GNATdoc that
      transform header files and ADS files into more human-friendly
      HTML files.)

* In some form, the software architectural design fully specifies:

  * All the software interfaces between software units (see
    Terminology section).
  * For each software unit:

    * The ASIL of the software unit.
    * All the software interfaces provided or used by the software
      unit.
    * All the software unit requirements (see Terminology section)
      allocated to the software unit apart from software interface
      specifications.

* There is a Configuration Management plan. This process requires the
  creation and maintenance of files. Except where stated otherwise,
  all files created and maintained in this process are subject to the
  Configuration Management plan, and it must be possible to refer to
  specific versions of specific files within specific work products.

* There are no requirements for availability that have ASILs higher
  than ASIL B.

Consistent ASIL
---------------

For each software unit, this process assumes that the requirements
allocated to the software unit, the unit design fragments of the
software unit, and any requirements on which the software unit depends
(e.g., requirements allocated to other software units via software
interface specifications) have ASILs as follows:

* All such requirements and design fragments that are related only to
  availability have the same ASIL, which is either ASIL B or the ASIL
  of the software unit itself, whichever is lower.
* All other such requirements and design fragments have the same as
  the ASIL of the software unit itself.

  * Note: These requirements and design fragments even include
    `Always_Terminates` contracts (and, by implication,
    `Forward_Progress` annotations), since `Always_Terminates`
    contracts are important not only for availability but also for
    establishing the feasibility of satisfying
    postconditions. Violation of an `Always_Terminates` contract
    could cascade into violation of other contracts, so it is not
    appropriate to assign a lesser ASIL to `Always_Terminates`
    contracts.

This eliminates any need for verification of consistency of ASILs in
formal requirements.

Assumptions About the Technical Architecture
--------------------------------------------

Primary Stack Guard Regions
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This process assumes that each task's primary stack has a guard
region, such that any attempt to access the guard region will result
in termination of the Ada partition.

The objective of a primary stack guard region is to detect when there
is insufficient space in the corresponding primary stack to satisfy a
primary stack allocation request, in such a way that the detection has
extremely low overhead (considering both code size and speed) and that
an allocation failure is detected before any corruption of unrelated
allocations occurs.

This objective is satisfied if both of the following criteria are met:

* Every primary stack allocation request size is no greater than the
  primary stack guard region size.
* A primary stack allocation request is not followed by a subsequent
  primary stack allocation request in the same task unless separated
  by at least one of the following:

  * An access to the primary stack space provided as a result of the
    earlier primary stack allocation request
  * Deallocation of that primary stack space

Non-SPARK Ada Assumptions
^^^^^^^^^^^^^^^^^^^^^^^^^

While this process does not mandate that Ada software be developed
according to this process, this process does assume that if any
non-SPARK Ada software is linked with software developed according to
this process, then the non-SPARK Ada software is reviewed for the
criteria defined in the :ref:`step-review-deactivated-spark` step.

Data Sharing Assumptions
^^^^^^^^^^^^^^^^^^^^^^^^

This process assumes that non-Ada software complies with SPARK
assumptions concerning data shared with SPARK code, as described in
the [ADA_EXTERNAL] GNATprove assumption and elaborated upon in the
[SPARK_EXTERNAL], [SPARK_ALIASING_ADDRESS], and [SPARK_EXTERNAL_VALID]
GNATprove assumptions.

Subprogram Contracts
^^^^^^^^^^^^^^^^^^^^

This process assumes that non-Ada software directly calling or called
from SPARK code complies with subprogram contracts, as described in
the [ADA_SUBPROGRAMS], [ADA_CALLS], and [ADA_OBJECT_ADDRESSES]
GNATprove assumptions.

Package Contracts
^^^^^^^^^^^^^^^^^

This process assumes that non-Ada software directly called from SPARK
code complies with package contracts, as described in the
[ADA_EXTERNAL_ABSTRACT_STATE] GNATprove assumption.

Data Contracts
^^^^^^^^^^^^^^

This process assumes that accesses to objects shared with SPARK via
objects declared with External_Name or Link_Name aspects are
consistent with the SPARK declarations, as described in the
[ADA_EXTERNAL_NAME] GNATprove assumption.

Note: This process makes this assumption even if all the accesses to
the object are in SPARK. All accesses to objects with External_Name or
Link_Name aspects imply the object is being shared outside the SPARK
boundary. Violation of this assumption can lead to GNATprove
unsoundness even in a program that consists entirely of SPARK code.

Function Purity Assumptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This process assumes that non-Ada software directly called from SPARK
code complies with the SPARK assumption that if a subprogram returns a
value but is not annotated with Volatile_Function, then the return
value must not depend on the address of any object.

Concurrency Assumptions
^^^^^^^^^^^^^^^^^^^^^^^

This process assumes that certain concurrency risks are adequately
mitigated in the software architectural design:

* This process assumes that the software architectural design ensures
  the absence of two or more concurrent calls to one or more SPARK
  subprograms that have conflicting permissions to the same object
  (the permissions are considered to conflict if at least one of the
  concurrently-executed SPARK subprograms has write permission). This
  assumption is necessary to address GNATprove assumptions
  [ADA_TASKING.1] and (in part) [PARTIAL_TASKING].

* This process assumes that the software architectural design ensures
  that SPARK code only calls protected entries or suspends on
  suspension objects if all callers (direct and indirect) are in
  SPARK, the calling task was defined in SPARK, and a single GNATprove
  run analyzes the former SPARK code, all callers (direct and
  indirect), and the definition of the calling task. This assumption
  is necessary to address GNATprove assumptions [ADA_TASKING.2a],
  [ADA_TASKING.2b], and (in part) [PARTIAL_TASKING].

Assumptions About Change Management
-----------------------------------

The :ref:`step-assign-requirement-unique-ids` process step assumes that all
changes, at least to the work products governed by this process, are
made in accordance with ISO 26262-8:2018, Clause 8 (Change
management).

In particular, this process assumes that per ISO 26262-8:2018, 8.4.4.1
prior to each change being made to work products, there is a
corresponding change request (such as a merge request submitted to a
configuration management system) that is evaluated by authorized
persons including at least:

* One developer involved with each affected work product that is not
  the author of the change request
* The project manager or safety manager for each affected work product

Assumptions About Software Interface Specifications
---------------------------------------------------

For each software interface provided or used by a software unit
developed according to this process, if the software interface is not
specified according to this process, then it is assumed that the
software interface is officially specified in an interface
specification or Interface Control Document (ICD). This latter
document must clearly identify:

* The obligations of each software unit that provides the software
  interface
* The obligations of each software unit that uses the software
  interface

A software interface specification can for example include content in
a combination of the following forms:

* Ada ADS files
* C/C++ header files
* A document containing natural language text, function prototypes,
  pseudocode, diagrams, etc.

Even if a software interface is not specified per this process, it can
still be implemented in Ada or SPARK. For example:

* The official interface specification can include ADS files that help
  specify the interface.
* The non-ADS content in the official interface specification can be
  transcribed into ADS files, through the Unit Design collection of
  process steps.

Ada/SPARK Process Binding
-------------------------

This process requires any organization observing it to have an
Ada/SPARK Process Binding document that specifies certain aspects of
how the process will be observed by that organization.

The Ada/SPARK Process Binding document must at a minimum achieve the
following objectives:

* Specify the location of the Ada/SPARK Guidelines (see next section).
* Specify the organization's methods for creating trace links when
  either end of the trace link is an entity in an ADS/ADB file, as
  specified in the Traceability Model section below.
* Specify the organization's methods and syntax for documenting
  control flow and data flow in semi-formal or formal notation in the
  design documentation fragments for ASIL C / ASIL D units in
  accordance with ISO 26262-6:2018, Table 5, bullets 1c and 1d.
* Specify the organization's procedure for performing control flow
  analysis and data flow analysis in accordance with ISO 26262-6:2018,
  Table 7, bullets 1f and 1g. This process specifies the conditions
  under which control flow analysis and data flow analysis must be
  performed, but this process does not specify the procedure for
  performing it.
* Specify the organization's methods and syntax for documenting unit
  design outside of ADS/ADB files.
* Specify the organization's requirements for global peer reviews.
* Describe test environment, which fulfills expectations listed in ISO
  26262-6:2018 9.4.5.

This process assumes that the Ada/SPARK Process Binding document has
been reviewed to ensure that it satisfies the above objectives.

Ada/SPARK Guidelines
--------------------

This process requires any organization observing it to have an
Ada/SPARK Guidelines document that specifies the intended usage of
Ada/SPARK language features.

The Ada/SPARK Guidelines document must at a minimum achieve the
following objectives:

* Specify guidelines on how to use Ada/SPARK to develop unambiguous
  and comprehensible software that achieves modularity, abstraction,
  and encapsulation, and which uses structured constructs, considering
  the following topics from ISO 26262-6:2018, 5.4.3 Table 1 "Topics to
  be covered by modeling and coding guidelines":

  * ISO 26262-6:2018, 5.4.3 Table 1 1b "Use of language subsets"
  * ISO 26262-6:2018, 5.4.3 Table 1 1e "Use of well-trusted design principles"
  * ISO 26262-6:2018, 5.4.3 Table 1 1g "Use of style guides"
  * ISO 26262-6:2018, 5.4.3 Table 1 1h "Use of naming conventions"
  * ISO 26262-6:2018, 5.4.3 Table 1 1i "Concurrency aspects"

* ISO 26262-6:2018, 8.4.5 Table 6 1a "Single exit recommendation"
* ISO 26262-6:2018, 8.4.5 Table 6 1f "Restricted use of pointers"
* ISO 26262-6:2018, 8.4.5 Table 6 1j "No recursions"

This process assumes that the Ada/SPARK Guidelines document has been
reviewed to be sufficient to ensure, in combination with this process,
compliance with the ISO 26262 objectives, requirements, and
recommendations.

Integration Verification
------------------------

This process assumes that, when integrating software containing
Ada/SPARK software units developed according to this process, the
Verification Plan and/or Verification Specification for verifying the
integrated software includes the verification activities specified in
the Integration Verification steps of this process, and specifies that
integration verification only passes if all the pass criteria in these
steps are met.

Also, the :ref:`step-run-integration-tests` step assumes the existence of
integration tests that are executed on the integrated software.
