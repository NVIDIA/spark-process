.. Copyright (C) 2024 - 2025 NVIDIA CORPORATION & AFFILIATES
.. Copyright (C) 2021 - 2024 AdaCore
..
.. Permission is granted to copy, distribute and/or modify this document
.. under the terms of the GNU Free Documentation License, Version 1.3 or
.. any later version published by the Free Software Foundation; with the
.. Invariant Sections being "Attribution", with no Front-Cover
.. Texts, and no Back-Cover Texts.  A copy of the license is included in
.. the section entitled "GNU Free Documentation License".

.. _sec-tracing-spark-assumptions:

=====================================
Traceability to GNATprove Assumptions
=====================================

This section provides evidence that if a software unit is developed
according to this process, then that software unit will satisfy all
the assumptions of GNATprove.

There is a complete list of assumptions made by GNATprove in [SUG]_,
section `Complete List of Assumptions
<https://docs.adacore.com/R/docs/gnat-25.1/spark2014/html/spark2014_ug/en/source/how_to_use_gnatprove_in_a_team.html#complete-list-of-assumptions>`_. The
assumptions are covered in the tables in the following subsections,
using the unique IDs of the assumptions that are specified in
[SUG]_. Where an assumption consists of multiple paragraphs and/or
multiple bullets, the assumption ID is followed by ".n[o]", where n is
the paragraph number (starting at 1), and o identifies the bullet
(starting at a). (None of the assumptions include nested bullets.)

For each fragment of each assumption made by GNATprove, the tables
below (1) trace the assumption fragment to the process step ID(s) that
ensure the assumption fragment is satisfied, and (2) provide a
justification that those process step(s) are sufficient to ensure that
the assumption fragment is satisfied.

Note: The GNATprove assumptions in this section are up-to-date with
the SPARK 24.1 documentation as of 2024-05-17.

Shorthand used by the GNATprove Assumptions
-------------------------------------------

In the GNATprove assumption tables, many assumptions use shorthand in
the Detailed Justification columns to avoid duplication of text. This
section explains the forms of shorthand sometimes used in the tables.

Shorthand for leveraging "guaranteed" warnings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this form of shorthand:

* The Process Step IDs That Comply column specifies the following
  step: :ref:`step-review-diagnostic-justifications`

* The Detailed Justification column fits the pattern "Guaranteed"
  GNATprove warning warning_text (where warning_text is one of the
  GNATprove warnings classified as "guaranteed" per [SUG]_)

This is shorthand for the following longer justification:

The :ref:`step-review-diagnostic-justifications` step requires a global peer
review for compliance with this assumption for each suppressed
warning_text GNATprove warning. Such GNATprove warnings are
"guaranteed" per [SUG]_.

Shorthand for leveraging GNATcheck rules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this form of shorthand:

* The Process Step IDs That Comply column specifies the following two steps:

  * :ref:`step-create-project-file`
  * :ref:`step-review-diagnostic-justifications`

* The Detailed Justification column fits the pattern

  GNATcheck rule rule (where rule is one of the GNATcheck rules listed
  in the Table of Required GNATcheck Rules in this document)

This is shorthand for the following longer justification:

The :ref:`step-create-project-file` step, via the "Requirements Concerning
GNATcheck Switches and Rules" section, requires GNATcheck to be
invoked with rule rule enabled.

The :ref:`step-review-diagnostic-justifications` step requires a global peer
review for compliance with this assumption for each suppressed
violation of GNATcheck rule rule.

Shorthand for peer review of Ada-specific concerns
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this form of shorthand:

* The Process Step IDs That Comply column specifies the following step:
  :ref:`step-review-deactivated-spark`

* The Detailed Justification column specifies:
  Peer review of non-SPARK Ada

This is shorthand for the following longer justification:

This assumption concerns interactions between SPARK code and non-SPARK
code for which either (a) the Ada language does not define a method of
interoperating with other languages (in which case the non-SPARK code
must specifically be non-SPARK Ada code) or (b) responsibilities of
other languages are separately justified below.

The :ref:`step-review-deactivated-spark` step requires peer review to ensure all
non-SPARK Ada entities comply with this assumption. This peer review
is required even for non-SPARK Ada software not developed according to
this process, as stated in the Non-SPARK Ada Assumptions section.

Terminology used by the GNATprove assumptions
---------------------------------------------

The assumptions "define a precisely supported address specification to
be an address clause or aspect whose expression is a reference to the
Address attribute on a part of a standalone object or constant."

The assumptions "define an imprecisely supported address specification
to be an address clause or aspect that is not a precisely supported
address specification."

The assumptions "define an object with an imprecisely supported
address to be either a stand-alone object with an address clause or
aspect that is an imprecisely supported address specification or an
object that is a reachable part of an object with an imprecisely
supported address (a component of a composite value or the designated
object of an access value)."

Generally Applicable Assumptions
--------------------------------

The following assumptions need to be addressed when using SPARK on all
or part of a program:

.. include:: tracing-all.inc

Assumptions For Mixing SPARK and Non-SPARK Code
-----------------------------------------------

The following assumptions need to be addressed when using SPARK on
only part of a program:

.. include:: tracing-part.inc

Assumptions For Modular Use of GNATprove
----------------------------------------

The following assumptions need to be addressed when calling GNATprove
on only part of a SPARK program at a time (either on an individual
unit or on a group of units), while providing only the specs of those
units that are not analyzed (not their bodies), so that the complete
SPARK program is analyzed by calling GNATprove multiple times with
different sets of unit bodies being available:

.. include:: tracing-modular.inc

Assumptions For Compiling SPARK With Non-GNAT Tools
---------------------------------------------------

GNATprove makes certain assumptions about the behavior of compilers
used to compile SPARK code. All of these assumptions are satisfied by
the GNAT compiler.

.. include:: tracing-compiler.inc

The :ref:`step-compile-project` step, which is used to compile SPARK code,
requires the use of GPRbuild.
