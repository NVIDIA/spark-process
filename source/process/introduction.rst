.. Copyright (C) 2024 - 2025 NVIDIA CORPORATION & AFFILIATES
.. Copyright (C) 2021 - 2024 AdaCore
..
.. Permission is granted to copy, distribute and/or modify this document
.. under the terms of the GNU Free Documentation License, Version 1.3 or
.. any later version published by the Free Software Foundation; with the
.. Invariant Sections being "Attribution", with no Front-Cover
.. Texts, and no Back-Cover Texts.  A copy of the license is included in
.. the section entitled "GNU Free Documentation License".

.. highlight:: spark

.. _sec-introduction:

============
Introduction
============

Disclaimer
----------

This document is a reference process whose initial version has been
developed jointly between NVIDIA and AdaCore, then reviewed by
TÜV-SÜD. It is not meant to represent the current stage of the NVIDIA
or AdaCore internal development and certification processes, nor does
it guarantee TÜV-SÜD acceptance or endorsement. Adjustments and edits
made past this initial version may be applied over time to reflect
evolution of the technology, state of the art, or feedback, and may
not receive systematic review from all the initial authors.

Foreword
--------

Adopting a new programming language is always a significant
challenge. It involves deploying a new environment, training teams to
a new formalism, adapting programming patterns, etc. However, at the
end of the day and from a process standpoint, programming languages
are vastly interchangeable. You will end up doing testing pretty much
in the same way, define requirements in the same way, perform static
analysis in the same way, etc. One would expect that such a change
will yield targeted improvement to a number of process entries, but
the way to develop software should remain mostly unchanged.

In that regard, Ada and SPARK is a different story. Considering it as
a language shift is a possibility, and this would certainly yield
value across a traditional development process. This would however
miss the key opportunity brought by the technology, the ability to
spin the development process to a verification driven process,
allowing to demonstrate software properties in a much more rigorous
and cost effective way than traditional methods.

Ada semantics are designed to minimize the risk of vulnerability and
maximize the semantic information defined directly in the source
code. SPARK leverages these attributes to provide a language that is
structurally exempt of a number of otherwise common vulnerabilities
and that allows defining additional properties to be formally verified
in place of dynamic testing. In SPARK, it is possible to guarantee
basic properties such as variable initialization, absence of buffer
overflow, range of data, or more generally what would otherwise end up
being defensive code, But it also provides means to define more
advanced requirements that can be expressed in the form of boolean
assertions, and against which an implementation can be formally
demonstrated to be correct without any need of running tests.

As for any technology, Ada and SPARK do not work in isolation but
rather in tandem with other environments. You may decide that some
pieces of code do not need the level of integrity that SPARK provides,
but should rather be written directly in non formally proven Ada. You
may decide that it's worthwhile to integrate newly written SPARK or
Ada code within a pre-existing C or C++ application, or that you want
to integrate externally developed libraries. The technology - and the
process - should account for that.

Developing code with formal verification in mind has an impact at
various levels in the development process. Establishing a way to
develop software in this way can be a long iterative path, with risks
of missing some key aspects of the technology. This document is meant
to allow new adopters to skip this, and start off an already
established process which has been reviewed by authorities and
experimented with by the industry. It is not meant to be used as-is -
but rather serve as a starting point for a customized process fit to
the specific situation of each individual organization.

Purpose of This Document
------------------------

This document defines a SPARK-based ISO-26262-compliant process for
developing a subset of the safety-critical vehicle software units to
ASIL D and to lower ASILs.

The process defined in this document applies exclusively to software
units that are developed entirely in the Ada programming language, but
is oriented towards software units for which some or all of the Ada
code complies with the SPARK subset. While some elements of this
process, such as required Ada compiler warning settings, may be
applicable to safety-critical Ada software development in general, a
software unit that mixes Ada with other languages (such as C, C++, or
assembly language) cannot be developed using this process.

This process covers the ISO 26262 requirements and objectives relevant
to language subsets, software unit design, software unit
implementation, and software unit verification. Additionally, the
process covers the ISO 26262 requirements and objectives related to
safety requirements when they are expressed in software interface
specifications.

This process supports formal verification and non-formal verification
side-by-side. A single software unit developed according to this
process can be formally verified in its entirety, non-formally
verified in its entirety, or partially formally verified and partially
non-formally verified.

The following topics, while important to address, are out of the scope
of this document:

* Software architectural design specification
* How to port an existing C/C++ software unit to this SPARK-based process
* Concurrency and concurrency-related topics
* Software safety analysis and DFA

Outline of the Rest of This Document
------------------------------------

* :ref:`sec-terminology` introduces terms needed to understand the
  rest of this document.

* :ref:`sec-process-assumptions` specifies some prerequisites for
  application of the process and some assumptions about surrounding
  processes.

* :ref:`sec-process` specifies the process itself.

* :ref:`sec-switches` specifies, for each of the tools required by the
  process, which tool switches must be present, which are prohibited,
  and which are optional, along with justifications.

* :ref:`sec-checklist` provides checklists to be used for verification
  according to this process.

* :ref:`sec-usage-analysis` enumerates the tools used by this process
  and determines their required TCLs.

* :ref:`sec-tracing-spark-assumptions` enumerates the assumptions
  GNATprove depends on for soundness and maps them, with
  justifications, to the process steps specified in
  :ref:`sec-process`.

* :ref:`sec-tracing-iso26262` identifies the portions of ISO 26262 that are
  addressed by this process and maps them, with justifications, to the
  process steps specified in :ref:`sec-process`.

* :ref:`sec-bibliography` provides links to various documents that are
  referenced by this process.

How To Read This Document
-------------------------

Most readers should read everything up to :numref:`sec-process`, and
:ref:`sec-checklist`. In addition:

* Engineers seeking to follow this process should typically review
  :ref:`sec-switches` and :ref:`sec-tracing-spark-assumptions`.

* Safety managers should typically review section
  :ref:`sec-usage-analysis`.

* The supplementary section :ref:`sec-tracing-iso26262` should only be
  consulted on an as-needed basis.
