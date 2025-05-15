.. Copyright (C) 2024 - 2025 NVIDIA CORPORATION & AFFILIATES
.. Copyright (C) 2021 - 2024 AdaCore
..
.. Permission is granted to copy, distribute and/or modify this document
.. under the terms of the GNU Free Documentation License, Version 1.3 or
.. any later version published by the Free Software Foundation; with the
.. Invariant Sections being "Attribution", with no Front-Cover
.. Texts, and no Back-Cover Texts.  A copy of the license is included in
.. the section entitled "GNU Free Documentation License".

Traceability Model
------------------

This section introduces the traceability model defined by the process
steps specified in the subsequent sections. The traceable entities
considered by this process include:

* Traceable entities introduced by this process:
   * Software unit requirements in ADS files
   * Software unit design fragments
   * Declarations (including subprogram bodies)
   * Diagnostic justifications and check suppressions
   * Software unit test cases

* Other traceable entities considered by this process:

  * Other software unit requirements (not in ADS files)
  * Fragments of other work products (e.g., software architectural
    design, software interface specifications, higher-level
    requirements, safety analyses, security analyses, etc.) that
    motivate software unit requirements

The trace links defined by this process include:

* Trace links from other work product fragments to software unit
  requirements in ADS files

  * Each non-formal unit requirement specified according to this
    process must trace to the material in other work products that
    motivates the unit requirement.
  * Note: This process permits unit requirements to be specified in
    other ways as well (outside of ADS files). This process does not
    impose constraints on the specification of unit requirements
    outside of this process, but in a typical safety process, some
    sort of justification will still be provided for each unit
    requirement that requires manual verification.

* Trace links from software unit requirements to software supporting
  software unit design fragments

  * Each non-formally-verified unit requirement allocated to the
    software unit, whether or not the requirement is in an ADS file,
    must trace to one or more unit design fragments that collectively
    satisfy the requirement.
  * For example, a trace link from a non-formal requirement in a
    non-SPARK interface specification (developed outside the scope of
    this process) to a formal unit design constraint in a SPARK
    ADS/ADB file that codifies the requirement in formal notation

* Trace links from software unit design fragments to supporting
  software unit requirements

  * Each non-formally-verified unit design fragment traces to zero or
    more unit requirements (e.g., allocated to other software units)
    that support the unit design fragment.

* Trace links from software unit design fragments to other supporting
  software unit design fragments

  * Each non-formally-verified unit design fragment traces to zero or
    more other unit design fragments that support the former unit
    design fragment.

* Trace links from software unit design fragments to declarations

  * Each non-formally-verified unit design fragment traces to zero
    more declarations that support the unit design fragment.

* Trace links from software unit requirements to software unit test
  cases

  * Each non-formally-verified unit requirement allocated to the
    software unit traces to zero or more software unit test cases
    that collectively verify the unit requirement.
  * Each unit test case traces to at least one motivating unit
    requirement or unit design fragment.

* Trace links from software unit design fragments to software unit
  test cases

  * Each non-formally-verified unit design fragment traces to zero or
    more software unit test cases that collectively verify the unit
    design fragment.
  * Each unit test case traces to at least one motivating unit
    requirement or unit design fragment (as was also mentioned
    earlier).

* Trace links from diagnostic justifications and check suppressions to
  software unit test cases

  * Each diagnostic justification and each check suppression traces
    to zero or more software unit test cases that collectively
    provide dynamic support for the diagnostic justification or check
    suppression.
  * Note: In contrast with unit requirements and unit design
    fragments, test cases are not developed to support diagnostic
    justifications and check suppressions; test cases that support
    diagnostic justifications and check suppressions are developed
    without consulting the implementation, and if this results in
    insufficient testing, then the unit design must be refined.

Assigning Traceability IDs to Content in ADS/ADB Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Note: This section uses the form of Extended Backus-Naur Form (EBNF)
notation and the S (white space) production defined by the W3C
Extensible Markup Language (XML) specification.

For purposes of establishing unambiguous trace links from/to specific
comments and syntactic constructs in ADS and ADB files, this process
defines a language for using comments to define local IDs for specific
comments and syntactic constructs in ADS and ADB files, and this
process defines rules for combining local IDs to form unique IDs.

The unique IDs defined by this process are hierarchical: For certain
kinds of syntactic constructs, when a local ID is assigned to an
entity within such a syntactic construct, the entity's unique ID is
the concatenation of the unique ID of that containing syntactic
construct, the dot character '.', and the entity's local ID (as with
Ada identifiers, local IDs are never permitted to contain the period
character '.'). For example, if local ID `My_Inner_Unique_Id` is
assigned to a comment directly contained within a subprogram whose
local ID is `My_Subprogram_Unique_Id`, which subprogram is in turn
directly contained within a library-level package with unique ID
`A.B.C`, then the comment's unique ID is
`A.B.C.My_Subprogram_Unique_Id.My_Inner_Unique_Id`.

For most kinds of syntactic constructs with local IDs (e.g., packages
and types), the local ID is exactly equal to the identifier that names
that syntactic construct. However, there are two exceptions to this
rule:

* Subprograms: Since subprograms can be overloaded, it is not always
  possible to use a subprogram's name as its local ID, so this process
  enables (but does not require) the local ID of a subprogram to be
  manually specified in comments. When a subprogram is not manually
  assigned a local ID, then its local ID is determined as follows:

  * If the subprogram's name is not overloaded, then the subprogram's
    local ID is its name.
  * If the subprogram's name is overloaded, then neither the
    subprogram nor any entity within it has a local ID. In this case,
    it is illegal to manually assign a local ID to any comment or
    syntactic construct within any declaration of the subprogram.

* Operators: Operators follow the same convention as subprograms, but
  with the additional difference that the name of an operator is of
  the form '"<other_special_character(s)>"', not an identifier.

Unique IDs are case sensitive, since trace links are broader than Ada
and, outside the context of Ada, most tools are case sensitive. To
ensure each entity has an unambiguous unique ID, this process requires
the use of the `-gnatyr` compiler switch (see section Requirements
Concerning Non-Warning-Related Compiler Switches).

:lrm:`2-7` defines a comment as two - characters, a sequence of zero
or more non-white-space characters, and an end-of-line. In EBNF:

.. code-block:: bnf

   comment ::= '-' '-' char_not_EOL* EOL
   char_not_EOL ::= [^#xD#xA]
   EOL ::= (#xD | #xA | #xD #xA | #xA #xD)

Each local ID is assigned with a comment block beginning with a start_comment:

.. code-block:: bnf

   start_comment ::= '-' '-' same_line_S? '@' start_tag same_line_S
                    '(' same_line_S? local_id same_line_S? ')' S?
   same_line_S ::= (#x20 | #x9)+
   start_tag ::=   'func'
               | 'proc'
               | 'pre_informal'
               | 'pre'
               | 'outcome_informal'
               | 'outcome'
               | 'type_contract_informal'
               | 'type_contract'
               | 'rule_informal'
               | 'doc'
               | 'justify'
   local_id ::= [A-Za-z_] [A-Za-z0-9_]*
   /* Reused from the XML spec */
   S ::= (#x20 | #x9 | #xD | #xA)+

The start_tag identifies what kind of entity is being assigned a local
ID:

* A func or proc tag is used to assign a local ID to a function or
  procedure, respectively. The next syntactic construct must be a
  subprogram declaration.
* A pre_informal, outcome_informal, type_contract_informal, or
  rule_informal tag is used to introduce a non-formally-specified
  obligation (requirement or unit design constraint). The next
  syntactic construct is not associated with the local ID.
* A pre, outcome, or type_contract tag is used to introduce a
  formally-specified obligation (requirement or unit design
  constraint). The next syntactic construct must be a Boolean
  expression or (for outcome tags only) an aspect or part of an aspect
  for a non-Boolean SPARK contract (such as a Global or Depends
  aspect). The tag applies to the largest syntactic construct that
  begins with the next token but does not include any tokens that
  occur after subsequent structured comments and, if the construct is
  a Boolean expression, is not itself an and then expression. (Note: A
  parenthesized expression is not an and then expression, even if it
  directly contains an and then expression.)
* A pre... tag is used to introduce a subprogram precondition. It must
  be used within a subprogram declaration. A precondition is an
  obligation of the caller of the subprogram.
* An outcome... tag is used to introduce a subprogram outcome, such as
  a postcondition or other contract concerning the subprogram's
  behavior. It must be used within a subprogram declaration. An
  outcome is an obligation of the subprogram body.
* A rule_informal tag is used in an external ADS file to introduce a
  specific obligation on the software outside the software unit that
  implements the external ADS file. The obligation is not tied to any
  specific subprogram or type declared in the external ADS file, so
  the obligation is imposed on that software regardless of what
  subprograms and types are used by that software.
* A doc tag is used to assign a local ID to a stand-alone
  documentation fragment embedded within a comment block in an ADS/ADB
  file.
* A justify tag is used to assign a local ID to a diagnostic
  justification or check suppression. The next syntactic construct
  must be a pragma.

A start_comment is optionally followed by a description, which extends
up to but not including the next Ada syntactic element or until the
end_comment, whichever comes first:

.. code-block:: bnf

   end_comment ::= '-' '-' same_line_S? '@' 'e' 'n' 'd'

The description is extracted from multiple-line comment blocks per the
following sequence of transformations, applied in the stated order:

#. The initial -- of each comment after the start_comment are stripped
   out.
#. Each EOL that is not followed by another EOL is replaced with a
   space (#x20).
#. Each sequence of multiple consecutive EOLs is replaced with a
   single EOL.
#. Each same_line_S sequence is replaced with a space (#x20), unless
   it is at the beginning of a line, in which case it is stripped.

Each description includes a short description, defined as follows:

* If the description includes a period character '.' that is
  immediately followed by S, then the short description consists of
  the part of the description extending up to and including the first
  such '.'.
* Otherwise, the short description consists of the entire description.
