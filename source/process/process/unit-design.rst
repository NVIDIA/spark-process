.. Copyright (C) 2024 - 2025 NVIDIA CORPORATION & AFFILIATES
.. Copyright (C) 2021 - 2024 AdaCore
..
.. Permission is granted to copy, distribute and/or modify this document
.. under the terms of the GNU Free Documentation License, Version 1.3 or
.. any later version published by the Free Software Foundation; with the
.. Invariant Sections being "Attribution", with no Front-Cover
.. Texts, and no Back-Cover Texts.  A copy of the license is included in
.. the section entitled "GNU Free Documentation License".

Unit Design
-----------

This section specifies process steps for unit design. The key
distinction in this process between unit requirements and unit design
is that unit requirements are directly visible outside the scope of
the software unit, whereas software unit design is internal to the
scope of the software unit (except for purposes of design analyses,
which are out of the scope of this process).

For software units developed according to process, the software unit
design can be specified in any combination of the following three
places:

* In the private parts of external ADS files.
* In all parts of internal ADS files.
* In ADB files, as long as all the unit design within each ADB file
  precedes all the unit implementation within that same ADB file, and
  there is a comment clearly identifying the end of the unit design
  and the beginning of the unit implementation.

.. _step-identify-activity-scope:

Identify Activity Scope
^^^^^^^^^^^^^^^^^^^^^^^

Select a software unit identified in the software architectural design
to which to apply this process. The scope of the application of this
process to that software unit will include the software requirements
allocated to the software unit, the software interfaces (whether or
not those software interfaces are developed according to this process)
provided or used by the software unit, and other properties,
constraints, or behaviors defined in the software architecture
specifications.

Note: The decision of whether or not to follow this software unit
development process can be made on a per-software-unit basis. This
process does not demand that any particular software unit be developed
according to this process, even for software units implemented in
SPARK.

Create (or otherwise ensure the existence of) a Software Unit
Verification Plan for the software unit. The Software Unit
Verification Plan must:

* State that the software unit is verified according to this process.

* State that this process (referring to this document) specifies part
  of the Verification Plan for the software unit.

* State that the Software Unit Verification Plan covers aspects of the
  Verification Plan for the software unit that are not covered by this
  process.

  * Note: These aspects will be added to the Software Unit
    Verification Plan in the :ref:`step-develop-unit-verification-plan` step.

* Identify the external non-nested packages to be implemented by the
  software unit, and their corresponding ADS file names. Note: The set
  of packages is determined by consulting the software interface
  specifications for the software interfaces identified in the
  software architectural design as being provided or used by the
  software unit, and then the ADS file names are determined based on
  the GNAT default file naming convention.

Also create (or otherwise ensure the existence of) a Software Unit
Verification Specification that states that it is the Verification
Specification for the software unit. This Software Unit Verification
Specification must also state that the aforementioned Software Unit
Verification Plan is the Verification Plan for the software unit and
that this process (referring to this document) specifies part of the
Verification Specification for the software unit. Test cases will
potentially be added to the Software Unit Verification Specification
in the :ref:`step-write-tests` step. Alternatively, if the software unit needs no
test cases, then this process can be cited as the Verification
Specification for the software unit, and then no Software Unit
Verification Specification work product needs to be developed for the
software unit.

Note: If the Software Unit Verification Specification is omitted for
now, be prepared to revisit this process step if and when later
process steps determine that test cases are needed. It is typically
not possible during this process step to be sure that no test cases
will be needed for a software unit, because:

* Formal verification of some properties might require more time than
  available, in which case those properties will need to be
  non-formally-verified instead.

* Even if the software unit itself is entirely formally-verified, the
  software unit might instantiate non-formally-verified generic
  packages or subprograms, in which case the generic test cases for
  the non-formally-verified generic packages or subprograms will need
  to be instantiated into test cases for the software unit.

Step ID: Identify_Activity_Scope

.. _step-create-project-file:

Create Project File
^^^^^^^^^^^^^^^^^^^

Create the unit project file, a project file for the software unit
that will define a set of switches to be used. In subsequent steps,
source directories and/or specific ADS/ADB files will be added to this
project file for the unit design (in the :ref:`step-create-internal-ads` step) and
unit implementation (in the :ref:`step-create-adb` step).

Note: Details on the definition of a project file and its content can
be found on [GTUG]_ (see in particular `Project File Reference
<https://docs.adacore.com/R/docs/gnat-25.1/gprbuild/html/gprbuild_ug/gprbuild_ug/gnat_project_manager.html#project-file-reference>`_
for the description of various project file constructs).

It is possible to start with a minimal project and add configuration
requirements along the way. For example, a minimal my_unit_project.gpr
could contain the following:

.. code-block:: gpr
   :caption: Example

   project My_Unit_Project is

      for Runtime ("Ada") use my_safety_qualified_runtime;
      for Target use my_target;

      package Builder is
        for Global_Configuration_Pragmas use "my_unit_project.adc";
      end Builder;

      package Compiler is
        for Default_Switches ("Ada") use ("switch", "switch", "switch");
      end Compiler;

      package Prove is
        for Proof_Switches ("Ada") use ("switch", "switch", "switch");
      end Prove;

      package Check is
         for Default_Switches ("Ada") use ("switch", "switch", "switch");
      end Check;

   end My_Unit_Project;

Note: The order of the attributes and packages above is not significant.

The project file must set the value of attribute Runtime("Ada") to a
safety-qualified runtime.

The project file must set the value of attribute Target to the
compilation target of the program.

Switches controlling GPRbuild operation itself rather than the
compiler, the binder, or the linker stages, must be set in the Builder
package. Note that some of these switches may nevertheless impact how
GPRbuild invokes the compiler, the binder, and the linker, thereby
affecting those stages. The Global_Configuration_Pragmas attribute
defines the filename containing the configuration pragmas. See step
:ref:`step-create-configuration-pragmas`.

Switches to be passed to the compiler must be set in the Compiler
package. The switches must comply with the Requirements Concerning
Compiler Warning Switches and Requirements Concerning
Non-Warning-Related Compiler Switches sections below and with any
restrictions in the Ada/SPARK Guidelines concerning style checking
switches.

Switches to be passed to GNATprove can be set in the Prove package or
passed on the gnatprove command line. (The -P and -U switches must be
specified on the gnatprove command line, but each of the other
switches can be specified in either location.) The GNATprove switches
in the Prove package must be limited to those permitted by the
Requirements Concerning GNATprove Switches section. Details on the
Prove project's attributes can be found on [SUG], section Project
Attributes.

Switches to be passed to GNATcheck can be set in the Check package or
passed on the gnatcheck command line. (The ``-P`` and ``-U`` switches
must be specified on the gnatcheck command line, but each of the other
switches can be specified in either location.) The GNATcheck switches
in the Check package must be limited to those permitted by the
Requirements Concerning GNATcheck Switches and Rules section.

If necessary, switches to be passed to the linker should be set in the
Linker package, and switches to be passed to the binder should be set
in the Binder package. These are not required by this process and are
not shown above in the minimal example of a project file.

No project file may contain a Naming package. The purpose of a Naming
package is to override GNAT file naming conventions. By instead
following GNAT file naming conventions, this process ensures that each
Ada/SPARK compilation unit is contained within a dedicated ADS or ADB
file, and that the particular compilation unit in each ADS file and
each ADB file can be inferred from its name.

In addition to the above constraints, no package may contain any
switches that are not safety-qualified.

Step ID: Create_Project_File

Deferred Creation of the Project File
"""""""""""""""""""""""""""""""""""""

The :ref:`step-create-project-file` step logically occurs after the
:ref:`step-identify-activity-scope` step. However, one can defer the actual
creation of the unit project file until later steps where the unit
project file is consumed as an input. One can also generate the unit
project file temporarily and on-demand as part of automated tooling
before each invocation of a program that consumes the unit project
file as an input. However, the options that will be used are logically
specified in this step, and must consistently be used in any unit
project file subsequently created for the software unit.

Unneeded Packages in Auto-Generated Project Files
"""""""""""""""""""""""""""""""""""""""""""""""""

If temporary unit project files are automatically generated on demand,
one can omit packages from temporary unit project files that are not
applicable to the tools that will be used with those particular
temporary unit project files. For example, if a temporary unit project
file is generated for the sole purpose of invoking GNATprove on a
software unit, then the Check package may be omitted from that
temporary unit project file.

Multiple Project Files For a Software Unit
""""""""""""""""""""""""""""""""""""""""""

A software unit can be split into multiple unit project files that
share the same switches and collectively cover all the ADS/ADB files
that contain the unit design and unit implementation, even if none of
the unit project files alone is sufficient to cover all the ADS/ADB
files that contain the unit design and unit implementation.

If multiple unit project files are used in this way, any step in this
process that entails executing a command on my_unit_project must be
understood as requiring a separate invocation of the command for each
unit project file. Many of the GNAT tools used by this process will
have the same aggregate effect regardless of how the project files are
divided, as long as the assumptions of this process are satisfied. The
GNATprove, GNATcheck, and CodePeer tools are exceptions to that rule,
but:

* While GNATprove makes some assumptions when invoked multiple times
  on distinct parts of the software, these are covered in the
  Traceability to GNATprove Assumptions section below.
* Any gaps in GNATcheck and CodePeer output resulting from different
  unit project file arrangements will be closed in the
  :ref:`step-automated-check-against-coding-std-integration` and
  :ref:`step-static-analysis-integration` steps below, which require an integrated
  project.

Multiple Software Units In a Project File
"""""""""""""""""""""""""""""""""""""""""

A unit project file can cover ADS/ADB files that are not part of the
software unit, for the same reason that a software unit can be split
over multiple unit project files. See the note in the :ref:`step-verify-project`
step that justifies this practice even when using GNATprove.

Refactoring Project File Packages
"""""""""""""""""""""""""""""""""

It is acceptable to use the GPR file ``with`` keyword to refactor unit
project files so that they share switches from a common source GPR
file.

.. _step-create-configuration-pragmas:

Create Configuration Pragmas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a global configuration pragmas file containing, at a minimum,
definitions of the user aspects required by this process (or ensure
that such a global configuration pragmas file has already been
created). Ensure that the global configuration pragmas file is
referenced in the project file, as the value of the attribute
``Builder'Global_Configuration_Pragmas``.

You may also create a project configuration pragmas file in which you
can define any user aspect definitions and language restrictions
required by your project.  If you do so, this project configuration
pragmas file should be referenced in the project file, as the value of
the attribute ``Compiler'Local_Configuration_Pragmas``.

Note: The GNAT toolchain requires consistent settings for certain
configuration pragmas across all object files linked together in a
given program or library. This implies that the settings of those
pragmas for your project must also be compatible with their settings
when they were used to build the Ada runtime library.

At a minimum, the global configuration pragmas file must contain the
following user aspect definition:

.. code-block:: ada

   pragma User_Aspect_Definition
     (Forward_Progress,
      Local_Restrictions (No_Secondary_Stack, No_Heap_Allocations),
      Always_Terminates);

Step ID: Create_Configuration_Pragmas

.. _step-identify-internal-packages:

Identify Internal Packages
^^^^^^^^^^^^^^^^^^^^^^^^^^

For each software unit, design zero or more internal non-nested
package hierarchies (or sub-hierarchies of existing non-nested
packages) that will specify the internal packages of the software
unit, if any. Record the names of all the software unit's internal
packages in the Software Unit Verification Plan, along with their
corresponding ADS file names per the GNAT default file naming
convention.

So that no software unit can access private declarations of another
software unit, ensure that at least one of the following conditions
applies for each external interface package (if any) that is an
ancestor of an internal package:

* The external interface package is part of a software interface
  specification that forbids the external interface package from
  having a private part.
* The external interface package is implemented by the software unit.

Step ID: Identify_Internal_Packages

Non-Necessity of Internal Packages
""""""""""""""""""""""""""""""""""

This process step allows for software units to have zero internal
package hierarchies, because a software unit can potentially satisfy
all its requirements without any internal packages if all the
following criteria are met by the software unit:

* The software unit provides or uses one or more software interfaces
  specified in the public parts of external ADS files.
* No internal interfaces are required to enable direct interaction
  between different non-nested packages in the software unit: Either
  the software unit implements a single non-nested package, or it
  implements multiple non-nested packages that don't directly interact
  with one another, or it implements multiple non-nested packages that
  only directly interact with one another via externally-visible
  interfaces of the software unit.
* If any non-formally-verified unit requirements are allocated to the
  software unit, then all the supporting unit design fragments reside
  in the private parts of the external ADS files or in the ADB files
  corresponding to the external ADS files.

Regarding the Transcription of Interfaces
"""""""""""""""""""""""""""""""""""""""""

Background: If a software unit provides, uses, or otherwise
participates in a software interface that was not specified in the
public parts of external ADS files as described in the Unit
Requirements process steps, but that software unit chooses to have Ada
code participate in that software interface (e.g., by using an Ada
subprogram body to implement part of the interface, or by using an Ada
subprogram declaration to call part of the interface), this process
treats this choice as a unit design decision, not a unit
implementation decision. See the portions of the
:ref:`step-declare-internal-types-states-and-subprograms` and
:ref:`step-capture-unit-design-constraints` steps concerning transcription of
interfaces.

This might suggest that such a software unit must have internal ADS
files into which to transcribe those interfaces. However, this process
allows unit design to be specified at the top of ADB files that
implement external ADS files, as long as there is a clear separation
in those ADB files between the unit design section and the unit
implementation section. Therefore, the participation of Ada code in
non-ADS-based interfaces does not necessitate that the software unit
have internal packages, because the interfaces can simply be
transcribed into declarations at the tops of ADB files.

Internal Package Naming Convention
""""""""""""""""""""""""""""""""""

Some of the examples in subsequent steps show a single package named
My_Unit_Name, which is intended to be an identifier corresponding to
the name of the software unit. However, this process allows a software
unit to have more than one internal package, and this process does not
constrain the names of those packages. It is important to recognize,
though, that the internal packages of a software unit are internal
design details of that software unit, and therefore the internal
packages of a software unit must not be referenced from other software
units via with clauses.

.. _step-create-internal-ads:

Create Internal ADS
^^^^^^^^^^^^^^^^^^^

For each internal package identified in step
:ref:`step-identify-internal-packages`, per the GNAT default file naming
convention, create an ADS file with name ${PACKAGE_FILE_NAME}.ads,
where PACKAGE_FILE_NAME is a file name derived from the package name
using the same conversion convention as in the :ref:`step-create-external-ads`
step. For example, if the full name of an internal package is
My_Unit_Name.My_Child_Name, then the corresponding ADS file name will
be my_unit_name-my_child_name.ads.

Internal packages should be declared with ``SPARK_Mode => On``:

.. code-block:: ada

   package My_Unit_Name.My_Child_Name
   with SPARK_Mode => On
   is
      ...
   end My_Unit_Name.My_Child_Name;

Ensure that the ADS file or its containing directory is identified as
source code in the unit project file.

Note: This process permits packages to be declared with ``SPARK_Mode
=> Off`` (or with no ``SPARK_Mode`` aspect at all). However, doing so
will increase the cost of verification in later steps.

Step ID: Create_Internal_ADS

.. _step-declare-internal-types-states-and-subprograms:

Declare Internal Types, States, and Subprograms
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For each software interface that the software unit provides or uses,
transcribe the non-ADS code fragments (e.g., C language declarations)
of the software interface specification that are applicable to the
software unit into equivalent declarations in the software unit design
sections of the software unit's ADS and/or ADB files.

For example, where a software interface specification specifies C/C++
data types and functions, use the appropriate Ada aspects to ensure
the Ada declarations are consistent with the software interface
specification (see [LRM]_, :lrm:`Interfacing with C and C++ <B-3>`).

Note: For software interfaces specified entirely through external ADS
files, the preceding paragraphs do not require any additional
development effort. However, for such software interfaces that were
not developed per this process, it can still be beneficial to
transcribe them into the software unit design for purposes of adding
contracts in the :ref:`step-capture-unit-design-constraints` step. For
example, a subprogram declared in an external ADS file could be
transcribed into a new subprogram declaration in the software unit
design, where the former subprogram merely calls the latter
subprogram.

Declare internal types, states, and subprograms (procedures and
functions) and define internal expression functions in the software
unit design sections of the software unit's ADS and/or ADB files until
the internal structure of the software unit is specified with
sufficient clarity to enable dynamic verification in later
steps. (These declarations are leveraged by the software unit design
and by the software unit implementation, but are not exposed to other
software units.)

Note: The degree to which dynamic verification is required by the
Dynamic Verification process steps, and by implication the number of
declarations that must be considered part of the software unit design
and not the software unit implementation, depends on the degree to
which formal verification is utilized. Since the degree to which
formal verification will be utilized is sometimes unknown at this
step, it can be necessary to revisit this step after the scope of
formal verification is finalized in the Unit Implementation step.

Step ID: Declare_Internal_Types_States_And_Subprograms

.. _step-capture-unit-design-constraints:

Capture Unit Design Constraints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For each software interface fragment transcribed into the software
unit design in the :ref:`step-declare-internal-types-states-and-subprograms` step,
determine which of the interface constraints in the software interface
specification are obligations of the software unit (and thus are
considered software unit requirements by this process), and attempt to
transcribe those interface constraints into formal contracts on the
transcribed declarations in the same manner as in the
:ref:`step-capture-requirements` step.

For each unit specification fragment (whether a unit requirement or a
unit design fragment, whether formal or non-formal, whether in
software interface specifications or non-unit-level work products or
unit design) other than the requirements transcribed into formal
contracts according to the previous paragraph, identify the
constraints pertaining to the internal types and subprograms
documented in the :ref:`step-declare-internal-types-states-and-subprograms` step
that are necessary to show that the unit's design satisfies the unit
specification fragment. For each such identified unit design
constraint, either formalize it with SPARK contracts or denote it
non-formally using a comment. Attempt to use SPARK contracts to
formalize unit design constraints, in the same manner as for unit
requirements as specified in the :ref:`step-capture-requirements` step.

Note: The previous paragraph is intentionally recursive. Introducing a
unit design constraint can result in a need for additional unit design
constraints. The recursion terminates when the unit design is
complete.

For traceability purposes, assign a unique ID to each
non-formally-verified unit design constraint (regardless of how it is
leveraged) and to each formally-verified unit design constraint that
is leveraged as part of non-formal verification of another unit
specification fragment. Assign unique IDs in the same manner as for
unit requirements as specified in the :ref:`step-assign-requirement-unique-ids`
step.

For each unit design constraint (whether formal or non-formal) that is
leveraged as part of non-formal verification of one or more other unit
specification fragments, create a trace link from the unit design
constraint to each non-formally-verified unit specification fragment
that the unit design constraint supports. Create trace links in the
manner specified in the Ada/SPARK Process Binding.

For each non-formally-verified unit design constraint, optionally also
create a trace link from the unit design constraint to each unit
requirement (whether allocated to the software unit or to another
software unit) that the unit design constraint directly depends
on. Such trace links are not necessary, but they can make incremental
reverification less expensive and can expose when requirements are no
longer needed.

Note: This step requires you to capture design constraints that
adequately support all the unit's specification fragments, even those
unit specification fragments that will be formally-verified. However,
this step does not require that you trace formal design constraints to
the formally-verified unit specification fragments they support,
because GNATprove will verify the sufficiency of those formal design
constraints in the :ref:`step-verify-project` step.

Note: It is beneficial to capture unit design constraints formally
even if it is known that the unit design constraints will be
non-formally-verified, because it is less expensive to develop test
cases for formal unit specification fragments than for non-formal unit
specification fragments (see the :ref:`step-write-tests` step).

Step ID: Capture_Unit_Design_Constraints

Revisiting This Step
""""""""""""""""""""

Unit design fragments are added in this step and in the
:ref:`step-document-design-solutions` step. Each time the unit design fragments
are modified, revisit this step to ensure that all necessary unit
design constraints are recursively identified.

The scope of formal verification is finalized in the Unit
Implementation steps. Each time a formal requirement or formal design
constraint is determined to be non-formally-verified instead of
formally-revisited, revisit this step to ensure that all necessarily
trace links exist.

Clean SPARK
"""""""""""

Conventionally, in order for two software units to coexist in the same
memory address space, they must be developed in their entirety to the
same ASIL. This follows from the fact that two software components can
only have different ASILs if the criteria for coexistence are met (ISO
26262-6:2018, 7.4.8), where the criteria for coexistence include the
absence of cascading failures from the software component that is of
lower ASIL (or QM) to a violation of a higher-ASIL safety requirement
allocated to the software component that is of higher ASIL (ISO
26262-9:2018, 6.4.3 and 6.4.4). A failure of one software unit could
result in:

* Stray memory writes that corrupt the memory of another software unit
  in the same memory address space.
* Unexpected subprogram calls that corrupt the state of objects in the
  same memory address space.
* Hangs or infinite loops that cause delays to the completion of
  another software unit in the same memory address space.

However, the risk that there will be faults or failures of a software
unit implemented in clean SPARK (see the definition of clean SPARK in
the Terminology section) that cascade into violations of safety
requirements of other software units in the same memory address space,
can be adequately controlled with a combination of:

* Safety analysis / DFA, to verify the absence of cascading failures
  resulting from intentional interaction between the software units
* GNATprove, to verify the absence of unintentional interaction
  between software units initiated by a clean SPARK unit
* The stack usage analyses done in the :ref:`step-check-stack-usage-unit` and
  :ref:`step-check-stack-usage-integration` steps

This justifies a reduction in the minimum required stringency of some
of the safety measures employed in the development and verification of
clean SPARK software units. Certain measures employed in the
development and verification of the software unit may be deployed in
accordance with the highest ASIL (if any) of all the non-formal
requirements imposed on the clean-SPARK software unit. This can in
particular reduce or eliminate the need for semi-formal notation in
unit design (see the :ref:`step-document-design-solutions` step) and it can reduce
or eliminate the need for structural coverage during unit tests (see
the :ref:`step-unit-test-run-and-coverage` step).

.. _step-document-design-solutions:

Document Design Solutions For Non-Formally-Verified Unit Specification Fragments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For each non-formally-verified unit specification fragment, use its
traceability to supporting unit design fragments (see the Traceability
Model section) to identify the supporting unit design constraints (if
any), and then evaluate whether these supporting unit design
constraints adequately support the former non-formally verified unit
specification fragment. The unit design constraints adequately support
the non-formally-verified unit specification fragment if test cases
that determine PASS/FAIL results on the basis of the unit
specification fragment and the supporting unit design constraints
alone would provide adequate coverage (see the
:ref:`step-unit-test-run-and-coverage` step) of the implementation.

If the unit design constraints do not adequately support the
non-formally-verified unit specification fragment, then document how
the unit is to satisfy the expectations stated in the
non-formally-verified unit specification fragment. The documentation
must specify, for example, how the unit design ensures correct data
flow and control flow both within the unit and between the unit and
other units.

Develop the documentation either in the form of comments in ADS/ADB
files, or outside of Ada files in the manner specified in the
Ada/SPARK Process Binding, or using a combination of the two
approaches. Ensure that any unit design documentation fragment within
an ADB file completely precedes the unit implementation within that
ADB file.

If the cleanliness-adjusted ASIL of the unit is ASIL C or ASIL D, then
any argumentation in this documentation that describes control flow or
data flow between more than three entities must be supported with
semi-formal notation (e.g., pseudocode or UML) or formal
notation. Specify any semi-formal notation or formal notation
according to the organization's methods and syntax (see the section
entitled "Ada/SPARK Process Binding").

If the cleanliness-adjusted ASIL of the unit is ASIL B or below, then
use any mixture of natural language and notations (whether informal,
semi-formal, or formal).

Assign a unique ID to each unit design documentation fragment. For a
unit design documentation fragment in an ADS or ADB file, assign each
unique ID using a structured comment with the syntax specified in the
Traceability Model section. For example:

.. code-block:: ada

   -- @doc (State_Machine_Doc) This fragment explains how the state
   -- machine works.
   --
   -- (Detailed documentation goes here)
   --
   -- @end

For each fragment of design solution documentation, create a trace
link (in the manner specified in the Ada/SPARK Process Binding) from
the documentation fragment to each non-formally-verified unit
specification fragment that the documentation fragment supports.

Note: Each non-formally-verified unit specification fragment should at
this point already have a unique ID to use for the trace links
required by the previous paragraph. This step ensures that every
fragment of design solution documentation has a unique ID, and the
:ref:`step-assign-requirement-unique-ids` and :ref:`step-capture-unit-design-constraints`
steps ensure that each non-formally-verified unit requirement and each
non-formally-verified unit design constraint developed per this
process has a unique ID. Not all of the unit requirements allocated to
the software unit are necessarily developed according to this process
(for example, unit requirements can potentially be found in software
architectural design), but this process assumes that a unique ID is
also assigned to each unit requirement developed outside this process,
so that all the trace links mandated by this step are between entities
with unique IDs.

For each fragment of design solution documentation, also create a
trace link (again, in the manner specified in the Ada/SPARK Process
Binding) from the documentation fragment to each subprogram that the
documentation fragment helps specify, and optionally to each unit
requirement (whether allocated to the software unit or to another
software unit) that the documentation fragment directly depends on
(see the corresponding suggestion in the
:ref:`step-capture-unit-design-constraints` for the benefits of including such
links). Create trace links in the manner specified in the Ada/SPARK
Process Binding.

Step ID: Document_Design_Solutions

ASIL vs. Cleanliness-Adjusted ASIL
""""""""""""""""""""""""""""""""""

If the cleanliness-adjusted ASIL of the unit is either QM, ASIL A, or
ASIL B, then this process does not require non-formal argumentation to
be supported with semi-formal notation, even if the unit is developed
to ASIL C or ASIL D. By definition, such a unit is implemented in
clean SPARK and each of its ASIL C and ASIL D requirements (if any) is
both formally specified and formally-verified. While the absence of
semi-formal notation can increase the likelihood of a systematic
fault, the risk that such a systematic fault will lead to the
violation of an ASIL C or ASIL D unit requirement is adequately
controlled by the use of GNATprove in the :ref:`step-verify-project` step, and the
risk that such a systematic fault will lead to the violation of an
ASIL C or ASIL D requirement outside the unit is already captured in
the unit requirements and their respective ASILs.

Note: Safety analysis and DFA must consider ASILs of specific safety
requirements allocated to the software unit, not just the ASIL to
which the software unit is developed, because those analyses would not
necessarily be re-executed if the software unit were subsequently
re-implemented as a multi-unit software component that allocates the
QM / lower-ASIL safety requirements to a QM / lower-ASIL unit.

The use of cleanliness-adjusted ASILs to determine unit design
documentation requirements does not constitute a deviation from
ISO 26262. In :ref:`ISO 26262-6:2018, Table 5
<iso-trace-p6-c8-4-3-t5-1c>`, the use of semi-formal notations is a
recommendation (and a high recommendation at ASIL C and ASIL D), not a
strict requirement. This process presents formal unit design
constraints as an alternative means of documenting the unit
design. When clean SPARK is used, GNATprove verifies the completeness
of these formal unit design constraints with respect to formal unit
requirements, obviating the need for semi-formal notations.

Traceability Not Required for Formally-Verified Unit Specification Fragments
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

This process does not mandate analogous unit design and unit
implementation traceability for formally-verified requirements and
formally-verified unit design constraints, because the risk that a
formally-verified unit design and unit implementation will fail to
comply with its formally-specified unit requirements and
formally-specified unit design constraints is sufficiently small that
there is minimal benefit in establishing such traceability. ISO 26262
and Automotive SPICE (the Quality Management standard presumed by this
process) collectively identify the following use cases for
traceability to software requirements, and all these use cases are
addressed through formal verification without the use of explicit
traceability:

* Verifiability (ISO 26262-6:2018, 7.4.2): The verifiability of
  formally-verified software requirements is established through
  successful formal verification by GNATprove of the design and
  implementation against those requirements.
* Consistency between a requirement, its implementation, and its
  verification (:ref:`ISO 26262-8:2018, 6.4.3.2
  <iso-trace-p8-c6-4-3-2-a>` note 2, first bullet; Automotive SPICE
  SWE.3.BP5, note 4, second objective): Formal verification by
  GNATprove establishes consistency of the design and implementation
  with the requirement, and by nature verifies the requirement exactly
  as specified (since the formal verification tool directly reads the
  formally-specified requirement, there is by nature negligible risk
  that GNATprove will misunderstand the requirement).
* Effectiveness of impact analysis if changes are made to a
  requirement or to the design/implementation (:ref:`ISO 26262-8:2018,
  6.4.3.2 <iso-trace-p8-c6-4-3-2-b>` note 2, second bullet; Automotive
  SPICE SWE.3.BP5, note 4, third objective): Any change to a
  formally-verified requirement, or to its design/implementation, that
  results in an inconsistency would result in GNATprove being unable
  to formally verify the requirement. Therefore GNATprove is a highly
  effective tool for impact analysis.
* Execution of confirmation measures (:ref:`ISO 26262-8:2018, 6.4.3.2
  <iso-trace-p8-c6-4-3-2-c>` note 2, third bullet): Given the minimal
  risk posed to safety by software that has been formally-verified, it
  is expected that confirmation measures will be focused primarily on
  non-formally-verified safety requirements. However, if a
  confirmation reviewer seeks to cross-check the effectiveness of the
  formal verification, since no target hardware is required to utilize
  GNATprove, the confirmation reviewer can directly modify the
  design/implementation in a way that is expected to cause a potential
  violation of a safety requirement subject to formal verification,
  and then the confirmation review can confirm by running GNATprove
  that in fact the formal verification fails.
* Coverage (Automotive SPICE SWE.3.BP5): Coverage exists to support
  verification and the identification of extraneous functionality. But
  GNATprove is able to complete formal verification without
  coverage. And the risk of extraneous functionality in
  formally-verified SPARK subprograms is very low, due to the fact
  that all side effects to global variables at unit boundaries must be
  exposed via Global contracts.

Revisiting This Step
""""""""""""""""""""

The scope of formal verification and the unit's clean SPARK status are
finalized in the Unit Implementation steps. Each time a formal
requirement or formal design constraint is determined to be
non-formally-verified instead of formally-revisited, revisit this step
to ensure that all necessary documentation exists. If the unit is not
clean SPARK, revisit this step to ensure that the documentation uses
semi-formal and formal notation where needed.

.. _step-inspect-unit-design:

Inspect Unit Design
^^^^^^^^^^^^^^^^^^^

With a local peer review, inspect (or otherwise review with similar
rigor) the unit design by completing the Verification Checklist for
Software Unit Design, to ensure that:

* The unit design is correct, complete, and consistent with respect to
  the non-formally-verified requirements.
* The unit design observes the Ada/SPARK Guidelines (except for
  guidelines automatically enforced via GNATcheck rules).
* The unit design is in-context-comprehensible to the inspector: The
  inspector understands the types, subprograms, unit design fragments,
  and non-formal argumentation sufficiently well to be able to
  understand how they support the unit requirements and to make
  changes to them as needed to accommodate future changes to the unit
  requirements.
* Control and data flow analysis is performed according to the
  Ada/SPARK Process Binding.
* The unit design only withs package specifications that are within
  the scope of the unit (external packages of interface specifications
  provided/used by the software unit and internal packages of the unit
  itself).

Record evidence of completion of the verification checklist in the
Software Unit Verification Report, identifying the peer reviewer(s)
and including the PASS/FAIL outcome in the final row of the checklist.

Step ID: Inspect_Unit_Design

Verification Work Products
""""""""""""""""""""""""""

ISO 26262 requires this verification to be done according to a
Verification Plan and Verification Specification. This process
partially defines the Verification Plan, the Verification
Specification, and what is expected in the Verification Report. This
process specifies where additional material must be developed in the
Software Unit Verification Plan and Software Unit Verification
Specification work products. See the :ref:`step-identify-activity-scope` step.

Implications and Timing of Unit Design Inspection
"""""""""""""""""""""""""""""""""""""""""""""""""

This step implicitly verifies the consistency of the
non-formally-verified unit requirements with one another, because if
there were any contradiction between different non-formally-verified
unit requirements, it would not be possible to specify a unit design
that satisfies all the non-formally-verified unit requirements.

This verification cannot be done earlier as part of specifying the
unit requirements for a software interface, because at that point not
all the unit requirements are known. A single software unit might
implement multiple software interfaces, and might receive requirements
from sources other than software interface specifications.

.. _step-verify-unit-design:

Verify Unit Design
^^^^^^^^^^^^^^^^^^

At this point, you have completed unit design. It is a good practice
to launch GNATprove in order to check consistency between the declared
data, the contracts, and the expression functions:

To run GNATprove, run the command:

.. code-block:: bash

   gnatprove -P my_unit_project -U

where ``my_unit_project`` is the name of the project file created in
the :ref:`step-create-project-file` step. The GNATprove verification report will
then be generated in gnatprove/gnatprove.out in your project's object
directory.

Fix any errors or warnings in the unit design in the private parts of
external ADS files, in internal ADS files, and in the unit design
portions of ADB files (where applicable). (For this process step,
disregard any errors or warnings related to the absence of
corresponding ADB files. If work has already begun on future process
steps, also disregard any errors or warnings pertaining to files added
in later process steps.)

During this step, you should be able to prove expression functions
that are defined in the specification files (as these functions
typically do not need an explicit postcondition, this is a proof of
absence of runtime errors).

Pass Criteria: GNATprove reports no warnings and no errors, except for
warnings and errors disregarded for this process step as described
above.

Step ID: Verify_Unit_Design
