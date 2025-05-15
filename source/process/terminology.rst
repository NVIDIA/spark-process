.. Copyright (C) 2024 - 2025 NVIDIA CORPORATION & AFFILIATES
.. Copyright (C) 2021 - 2024 AdaCore
..
.. Permission is granted to copy, distribute and/or modify this document
.. under the terms of the GNU Free Documentation License, Version 1.3 or
.. any later version published by the Free Software Foundation; with the
.. Invariant Sections being "Attribution", with no Front-Cover
.. Texts, and no Back-Cover Texts.  A copy of the license is included in
.. the section entitled "GNU Free Documentation License".

.. _sec-terminology:

===========
Terminology
===========

Software Unit (or Unit)
-----------------------

A software unit, or unit for short, is a software component that is
treated as atomic for purposes of ISO 26262. In this process, except
where explicitly specified otherwise, the terms software unit and unit
refer specifically to software components developed according to this
process.

Note: The definition of software unit in ISO 26262 is an "atomic level
software component of the software architecture that can be subjected
to stand-alone testing" (ISO 26262-1:2018, 3.159).

Each software unit (specifically, each software unit's design and
implementation) developed according to this process includes:

* The private parts of zero or more external ADS files.

* Zero or more internal ADS files.

* Zero or more ADB files.

 * A software unit that includes one or more ADB files can potentially
   be compiled into one or more object files.

 * A software unit that does not include any ADB files is not compiled
   into object files. With the GNAT toolchain supported by this
   process, only ADB files can be compiled. (Note: Such a software
   unit consists only of the private parts of external ADS files. A
   software unit with no ADB files cannot include internal ADS files,
   because there would be nothing to with the specifications in those
   internal ADS files.)

Unit-Level Work Product
-----------------------

A unit-level work product is a work product developed or directly
influenced by software unit development.

Examples of unit-level work products include:

* Software interface specifications
* Software unit design (SWUD)
* Software unit implementation
* Software unit verification plans (SWVP)
* Software unit verification specifications (SWVS)
* Software unit verification reports (SWVR)

Non-Unit-Level Work Product
---------------------------

A non-unit-level work product is any work product that is not a
unit-level work product. Examples of non-unit-level work products
include, but are not limited to:

* HSI specifications
* The software architectural design
* Software unit requirements specifications other than software
  interfaceq specifications
* Abstractions of software interface specifications
* Non-unit-level requirements (requirements on higher-level software
  elements)
* Safety and security analyses

Note: The development of non-unit-level work products is largely out
of the scope of this process.

Software Unit Specification Fragment (or Unit Specification Fragment)
---------------------------------------------------------------------

A software unit specification fragment, or unit specification fragment
for short, is a software unit requirement or a software unit design
fragment.

Software Unit Requirement (or Unit Requirement)
-----------------------------------------------

A software unit requirement, or unit requirement for short, is any of
the following:

* A safety requirement allocated by the software architectural design
  to the software unit, including the ASIL of the safety requirement.
* A non-safety (QM) requirement or any other kind of constraint
  imposed by the software architectural design on the software unit.
* An expectation that a software unit will provide or use a software
  interface.
* An obligation imposed on a software unit via a hardware/software
  interface (HSI) specification.
* An obligation imposed on a software unit via a software interface
  specification.
* State the software unit is expected to have.
* An invariant the software unit is expected to maintain.
* Other behavior of the software unit that is expected to be visible
  at the software unit's boundaries.
* Any other requirement allocated to the unit with an applicable
  software requirements management tool.

A software unit requirement is, abstractly, a property of the software
unit that is intended to be understood and relied upon by software
outside the software unit.

Software Unit Design Fragment (or Unit Design Fragment)
-------------------------------------------------------

A software unit design fragment is a software unit design constraint
or a design documentation fragment.

Note: Software unit design fragments are classified based on whether
they are tied to specific syntactic constructs (software unit design
constraints) or not (design documentation fragments).

Software Unit Design Constraint (or Unit Design Constraint)
-----------------------------------------------------------

A software unit design constraint, or unit design constraint for
short, is any constraint imposed on a specific syntactic construct of
the software unit implementation by the software unit design, but not
imposed by the software unit requirements.

A software unit design constraint is, abstractly, a property of a
syntactic construct of the software unit that is not intended to be
understood or relied upon by software outside the software unit.

Examples of software unit design constraints:

* Contracts specified for internal packages and subprograms (these are
  an example of formal software unit design constraints)
* Non-formal constraints for internal packages and subprograms

Design Documentation Fragment
-----------------------------

A design documentation fragment is a property of the software unit
design not tied to a specific syntactic construct that is nevertheless
important for satisfying one or more software unit requirements and/or
complying with one or more other software unit design fragments. Each
design documentation fragment consists of either (1) a single block of
comments in an ADS/ADB file or (2) content outside of ADS/ADB files
that is not constrained by this process (but is constrained by the
Ada/SPARK Process Binding).

Diagnostic Justification
------------------------

A diagnostic justification is a pragma that suppresses certain GNAT
tool diagnostics and an associated natural-language justification for
why the suppression is permissible. The precise set of pragmas that
constitute diagnostic justifications is defined in the
:ref:`step-review-diagnostic-justifications` step.

Check Suppression
-----------------

A check suppression is a pragma that suppresses certain GNAT runtime
checks. The precise set of pragmas that constitute check suppressions
is defined in the :ref:`step-review-deactivated-spark` step.

Formal Unit Requirement or Formal Unit Design Constraint
--------------------------------------------------------

A formal unit requirement or formal unit design constraint is a unit
requirement or unit design constraint, respectively, that is specified
formally using SPARK annotations.

Non-Formal Unit Requirement or Non-Formal Unit Design Constraint
----------------------------------------------------------------

A non-formal unit requirement or non-formal unit design constraint is
a unit requirement or unit design constraint, respectively, that is
specified without using SPARK annotations. (A non-formal unit
requirement or non-formal unit design constraint is typically
expressed using natural language and/or semi-formal notation.)

Implementation Free Requirement
-------------------------------

According to :ref:`ISO 26262-8:2018 6.4.2.4h
<iso-trace-p8-c6-4-2-4-h>`, an implementation free requirement, while
addressing what is necessary and sufficient for the item, avoids
placing unnecessary constraints on the architectural design. The
objective is to be implementation independent. The requirement states
what is required, not how the requirement should be met.

Software Interface
------------------

A software interface (sometimes interface for short) is a set of
syntactic entities and associated constraints that connect two or more
software units, where at least one of the software units provides the
interface and at least one of the software units uses the interface (a
software interface is by definition asymmetric). Each software unit
provides zero or more (but typically one or more) software interfaces
and uses zero or more software interfaces.

Each software interface can optionally be specified according to this
process.

A software specified according to this process is specified in the
form of one or more external ADS files, subject to various
restrictions defined in this process. A software interface specified
per this process in the form of external ADS files combines:

* declarations of packages, types, constants, variables, states,
  and/or subprograms,
* an indication of which package/subprogram bodies or type extensions
  are to be implemented by the provider(s) of the interface and which
  are to be implemented by the user(s) of the interface,
* formal unit requirements specified using SPARK contracts (Pre, Post,
  etc.), and
* non-formal unit requirements associated with those packages, types,
  and/or subprograms.

A software interface not specified according to this process must
satisfy the assumptions in section Assumptions About Software
Interface Specifications (such as the need for each software interface
to clearly distinguish between the obligations of software units that
provide the interface and software units that use the interface), but
such software interfaces are otherwise not restricted by this process.

SPARK Platinum
--------------

An Ada syntactic construct is referred to as being SPARK Platinum if
both of the following conditions hold:

* The construct is part of ``SPARK_Mode => On`` Ada code but not part
  of ``Annotate => (GNATprove, Skip_Proof)`` or ``Annotate =>
  (GNATprove, Skip_Flow_And_Proof)`` code.

* All of the requirements and design constraints applicable to the
  syntactic construct are formal; the construct has no non-formal
  requirements or unit design constraints.

A software interface is referred to as being SPARK Platinum if all of
the following conditions hold:

* The software interface is specified according to this process, using
  external ADS files.
* All of the requirements specified in the external ADS files are
  formal requirements.
* All of the software interfaces specified in external ADS files
  with'd by the external ADS files are themselves SPARK Platinum.

A software unit is referred to as being SPARK Platinum if both of the
following conditions hold:

* All of the software interfaces provided or used by the software unit
  are SPARK Platinum.
* ``SPARK_Mode`` is set to ``On``, and ``Annotate => (GNATprove,
  Skip_Proof)`` and ``Annotate => (GNATprove, Skip_Flow_And_Proof)``
  are not used, across the entirety of all the compilation units that
  make up (or external ADS files with private parts, contribute to)
  the software unit design and implementation.

Clean SPARK
-----------

A software unit is said to be implemented in clean SPARK if none of
the constructs identified in the Review Diagnostic Justifications and
Review Deactivated SPARK steps as requiring manual review exist
anywhere in any of the ADS and ADB files that make up the software
unit.

Clean SPARK Platinum
--------------------

A software unit is said to be implemented in clean SPARK Platinum if
the software unit is SPARK Platinum and is implemented in clean SPARK.

Cleanliness-Adjusted ASIL
-------------------------

Each software unit has a cleanliness-adjusted ASIL used to determine
the level of rigor of certain verification measures. A software unit's
cleanliness-adjusted ASIL is determined as follows:

* If the software unit is implemented in clean SPARK, then the
  cleanliness-adjusted ASIL of the software unit is the highest of all
  the ASILs of all the non-formal safety requirements allocated to the
  software unit, or QM if all non-formal requirements allocated to the
  software unit are QM.
* Otherwise (if the software unit is not implemented in clean SPARK),
  the cleanliness-adjusted ASIL of the software unit is equal to the
  ASIL to which the software unit is developed, or QM if the software
  unit is not developed to any ASIL.

GPR File (or Project File)
--------------------------

A GPR file is a file whose path ends with ".gpr". With the GNAT tools,
GPR files are used to describe projects.

Unit GPR File (or Unit Project File)
------------------------------------

The unit GPR file (or unit project file) for a software unit is the
GPR file (project file) used when invoking the GNAT tools to indicate
the ADS/ADB files and configuration settings for the software unit.

Note: As discussed in the :ref:`step-create-project-file` step, several variations
are permitted by this process. A software unit's ADS/ADB files can be
spread over multiple GPR files, multiple software units can be covered
by the same GPR file, and GPR files can be generated automatically
on-demand.

ADC File
--------

An ADC file is a file whose path ends with ".adc". With the GNAT
tools, ADC files are used to specify configuration pragmas.

ADS File
--------

An ADS file is a file whose path ends with ".ads". With the GNAT
tools, ADS files are used to contain specifications for packages and
subprograms.

ADB File
--------

An ADB file is a file whose path ends with ".adb". With the GNAT
tools, ADB files are used to contain bodies for packages and
subprograms.

External ADS File
-----------------

An external ADS file is an ADS file that is part of a software
interface specified per this process.

Internal ADS File
-----------------

An internal ADS file is an ADS file that is not an external ADS file.

GNAT Project (or Project)
-------------------------

A GNAT Project (or project for short) is the combination of a GPR file
and all the ADC, ADS, and ADB files that are referenced in the GPR
file (whether explicitly by full path, or implicitly by containing
directory).

Non-Formal Verification
-----------------------

The non-formal verification measures include both static verification
measures such as code inspection and dynamic verification measures
such as dynamic testing.

Formally-Verified
-----------------

A formal unit requirement (in the context of a particular software
unit to which the formal unit requirement is allocated) or formal unit
design constraint is said to be formally-verified if all the entities
in the software unit that are obligated to comply with the formal unit
requirement or formal unit design constraint have the ``SPARK_Mode``
aspect set to ``On`` and do not have aspect ``Annotate => (GNATprove,
Skip_Proof)`` or ``Annotate => (GNATprove, Skip_Flow_And_Proof)``.

The applicable entities vary depending on the particular kind of unit
requirement or unit design constraint. For example:

* If the formal unit requirement or formal unit design constraint
  consists of part or all of the aspect definition of a ``Pre`` or
  ``Pre'Class`` aspect of a subprogram or access-to-subprogram type,
  then the applicable entities are all the declarations and executable
  bodies in the software unit that call that subprogram or call
  through values of that access-to-subprogram type.

* If the formal unit requirement or formal unit design constraint
  consists of part or all of the aspect definition of any other
  contract aspect of a subprogram or access-to-subprogram type, then
  the applicable entities include:

   * For a subprogram:
      * The body of the subprogram, if it is part of the software unit.
      * The declarations of all overriding subprograms in the software
        unit, if the subprogram is a dispatching primitive.

   * For an access-to-subprogram type:
      * All the executable bodies in the software unit that assign
        values to objects of that access-to-subprogram type.

* If the formal unit requirement or formal unit design constraint
  consists of part or all of a type contract for a particular type,
  then the applicable entities are all the declarations and executable
  bodies in the software unit that assign values to objects of that
  type (including assignments of actual parameters to formal
  parameters as part of subprogram calls, and including values
  returned from functions).

* If the formal unit requirement or formal unit design constraint
  consists of part or all of a package contract, then the applicable
  entities are all the executable bodies within the part of the
  package including the contract and subsequent parts of the same
  package.

Note: If a software unit contains any entities that have ``SPARK_Mode``
set to ``Off`` or that have ``Annotate => (GNATprove, Skip_Proof)`` or
``Annotate => (GNATprove, Skip_Flow_And_Proof)`` aspects, it can be
tedious to determine whether each of the formal unit requirements and
formal unit design constraints are formally verified with respect to
the software unit. For this reason and others, the
:ref:`step-implement-spark-package` step (see below) recommends that ``SPARK_Mode``
be turned on wherever possible and that ``Annotate => (GNATprove,
Skip_Proof)`` and ``Annotate => (GNATprove, Skip_Flow_And_Proof)`` be
avoided wherever possible.

Note also: A unit design fragment can only be formally-verified if the
unit design fragment is specifically a unit design constraint.

Non-Formally-Verified
---------------------

A unit requirement (in the context of a particular software unit to
which the unit requirement is allocated) or unit design fragment is
non-formally-verified if it is not formally-verified.

Note: Each unit design fragment is either a unit design constraint or
a design documentation fragment (see the definition of unit design
fragment), but of these, only a unit design constraint can be
formally-verified (see the definition of formally-verified). Therefore
every design documentation fragment is by definition
non-formally-verified.

Note: A unit specification fragment that is formally specified in
ADS/ADB files per the :ref:`step-capture-requirements` or
:ref:`step-capture-unit-design-constraints` step can only be non-formally-verified
with respect to the software unit if at least one of the entities in
the software unit to which the formal unit specification fragment
applies does not have the ``SPARK_Mode`` aspect set to ``On`` or does
have aspect ``Annotate => (GNATprove, Skip_Proof)`` or ``Annotate =>
(GNATprove, Skip_Flow_And_Proof)``.

Out-of-Context-Comprehensible
-----------------------------

A work product fragment is out-of-context-comprehensible to a
particular person if that person could, if asked, do both of the
following:

#. Specify the precise meaning of the work product fragment.
#. Modify the work product fragment, along with other work product
   fragments if necessary, in order to maintain correctness,
   completeness, and consistency with new versions of input work
   products.

Note: A work product fragment is only comprehensible to a particular
person if that particular person states that it is.

Note: Reviewers are often asked to confirm the comprehensibility of
work product fragments to them. Reviewers need not, and typically
don't, do any of the above activities as part of confirming
comprehensibility. These are hypothetical activities used to define
objective criteria that a reviewer can use to determine whether a work
product fragment is comprehensible. However, while the criteria
themselves are objective, the decision of comprehensibility is
inherently subjective, since the criteria are evaluated in the context
of a particular reviewer.

In-Context-Comprehensible
-------------------------

A work product fragment is in-context-comprehensible to a particular
person if both of the following criteria are satisfied:

#. The work product fragment is out-of-context-comprehensible to that
   person.
#. That person could, if asked, do both of the following:

   #. Develop an argument for the correctness and completeness of the
      work product fragment against the input work products,
      especially against the input work product fragments to which the
      considered work product fragment traces.
   #. Develop an argument for the consistency of the work product
      fragment within the containing work product.

Local Peer Review
-----------------

A local peer review is a review of technical content by one or more
reviewers that meet both of the following criteria:

* The reviewer must have sufficient technical expertise to conduct the
  review.
* The reviewer must not be an author of the material being reviewed.

Importantly, in a local peer review, the reviewer(s) can (but does not
have to be) members of the same team as the author(s).

Global Peer Review
------------------

A global peer review is a review of technical content by one or more
reviewers that meet all of the following criteria:

* Both the criteria for reviewers conducting local peer reviews.
* Any additional criteria defined by the Ada/SPARK Process Binding.
