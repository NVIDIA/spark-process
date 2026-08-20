<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION &
                        AFFILIATES. All rights reserved.
-->

# Types in Ada/SPARK projects

Consistent and good use of types is one of the most important success
criteria in a Ada/SPARK project.

The purpose of types is twofold: they describe the data carried by a
variable, and they serve as implicit pre- and post-conditions. Both
serve to avoid errors before they occur. In SPARK terms, the
definition of a type is essentially a gold/platinum property, while
the implicit contracts (ranges and/or predicates) usually are a silver
property (but could also be gold/platinum).

## No built-in types

The main guidance is this: an Ada/SPARK project must not use any
built-in Ada types, except in a few circumstances:

* `Boolean` and `String` are always OK to use. In fact you really must
  not create project specific versions of these.
* `Integer` (and its subtypes `Natural` and `Positive`) can be used
  when interfacing with `Strings`, or other parts of the standard
  library (e.g. `Ada.Numerics.Elementary_Functions`)
* When creating maths functions (e.g. a square root function)
* `Unsigned_8` (or a user-defined type like `Byte`) can be used to
  describe opaque buffer contents where we don't actually care what is
  inside (e.g. crypto or compression)
* When writing a thin binding for interfacing with C - but make sure
  that the SPARK facing interface does not use these types.

> [!TIP]
> Relevant GNAT Check rules:
> [Predefined_Numeric_Types](https://docs.adacore.com/live/wave/lkql/html/gnatcheck_rm/generated/predefined_rules.html#predefined-numeric-types)
> (although this rule can be too strict at times).

## Don't re-create the built-in types

Sometimes these rules are side-stepped by projects creating their own
version of these types, e.g:

```ada
type Int is range -2**31 .. 2**31 - 1;
```

Don't do this. This is malicious compliance: dodging the intent of
this guidance.

Note: it is not wrong to create full-range types as long as it's clear
they are representing some physical unit. For example:

```ada
type Seconds is range 0 .. Integer'Last;

type Meters is digits 6;
```

## Use Boolean for boolean data

Use the built-in `Boolean` type whenever you have a yes/no,
enabled/disabled, valid/invalid kind of situation.

For example, don't create types like this:

```ada
type Active_Status (Disabled, Enabled);   -- don't do this
```

Instead, you describe the property:

```ada
type Information is record
   Safety_Enabled : Boolean;
end record;
```

That way the if-test is a bit more readable:

```ada
if Something.Safety_Enabled then
```

### Avoid three-valued logic

On the subject of `Boolean`: avoid three-valued logic, especially when
porting from C. It is a common pattern in some safety critical code to
do things like this:

```c
if (status == potato_true) {
   ...
} else if (status == potato_false) {
   ...
} else {
   log_an_error;
}
```

This is completely unnecessary in SPARK:

* Just use a `Boolean`
* When reading data from the outside world (this includes your
  interfaces to C programs) just validate the data (SPARK will force
  you to do this if your interface is in SPARK).

## Separate data in separate types

The primary purpose of types is to separate different data. The
classic example is this:

```ada
type Meters is digits 6;
type Feet is digits 6;
```

Here it is entirely obvious because the units are different. But this
also applies to e.g. counting types:

```ada
type Packets is range 0 .. 1024;
type Users   is range 0 .. 1024;
```

While both of these types count, they count different things and
assigning one to the other doesn't make sense.

Note that the common pattern of index and counting types is not
_really_ an exception to this rule -- both really are an offset, and
one excludes 0.

```ada
type Count_T is range 0 .. 100;
subtype Index_T is Count_T range 1 .. Count_T'Last;
```

## Sub-types to describe properties

Sub-types should be used when describing values of a type with special
constraints. Sub-types should be preferred over pre- and
post-conditions whenever possible.

For example instead of:

```ada
type Id is range 0 .. 1000;

procedure Do_Something (Person : in Id)
with Global => (In_Out => Database),
     Pre => Id /= 0;
```

You should introduce a subtype:

```ada
type Id is range 0 .. 1000;
subtype Valid_Id is Id range 1 .. Id'Last;

procedure Do_Something (Person : in Valid_Id)
with Global => (In_Out => Database);
```

If the constraint is more complicated you can use predicates:

```ada
type Id is range 0 .. 1000;

function Is_Valid_Id (Person : Id) return Boolean;

subtype Valid_Id is Id
with Predicate => Is_Valid_Id (Valid_Id);

procedure Do_Something (Person : in Valid_Id)
with Global => (In_Out => Database);
```

## Use of private types

Private types and limited private types are an excellent way to ensure
low coupling and high cohesion. However do not be religious about it:
private types are encouraged when they make sense but they should not
be used above all other concerns.

For example:

```ada
type Coordinate is private;
```

This makes no sense - you probably want to manipulate the X and Y
component all the time. If you need special constraints to hold in
some places you can subtype the record and add a predicate.

Private types should be used if:

* You want to statically rule out certain programming errors /
  behaviours, specifically if you want rely on some invariant you
  establish

* Nobody will care about the internals

The classic example is a stack:

```ada
package Stacks
is
   type Size_T is range 0 .. 100;

   type Stack is private;

   --  API

private

   subtype Index_T is Size_T range 1 .. Size_T'Last;

   type Content_T is array (Index_T) of Some_Element_Type;

   type Stack is record
      Top     : Size_T;
      Element : Content_T;
   end record;

end Stacks;
```

Perhaps we want to implement the `Clear` procedure for performance
reasons like so:

```ada
   procedure Clear (S : out Stack)
   is
      pragma Annotate (GNATprove, Intentional, "* is not initialized",
                       "we ensure in other functions that we never" &
                       " access beyond Top");
   begin
      S.Top := 0;
   end Clear;
```

This justification is only defensible if no other code can manipulate
the stack.

### Generics and private types

A special note should be added on the interaction between generics and
private types. When creating a generic, you should try to define as
many types as possible outside the generic. This is especially true if
any of the types are a private type.

This is a classic example of this problem:

```ada
generic
   ...
package Some_Crypto

   type Buffer is array (Positive range <>) of Byte;
end Some_Crypto;

package Cypto_Version_1 is new Some_Crypto (Param => ...);
package Cypto_Version_2 is new Some_Crypto (Param => ...);
```

In this example, the `Buffer` type is created every time you
instantiate the generic. These copies are incompatible. This means
when using version 1, you cannot use a buffer from version 2 without
explicitly converting. This type should be defined outside, in a
separate type package.

## Type packages

When structuring your project, you should declare types in appropriate
locations. The guidance is:

* Avoid duplication at all costs
* Use type packages for common types
* Declare complex types in packages where they are used
* Limit scope

A _type package_ is a package that just declares types, constants, and
perhaps predicates and conversion functions. Often these packages are
marked `Pure`.

For example:

```ada
package Types
with Pure
is

   type Seconds is new Long_Integer;

   type Nano_Seconds is new Long_Integer;

   Nano_Seconds_Per_Second : constant := 1_000_000_000;

end Types;
```

You can create more type packages that build on these generic types:

```ada
package Types.Command_Line_Parameters
is

   subtype Max_Delay_Time is Seconds range 0.0 .. 5.0;

end Types.Command_Line_Parameters;
```

Types that are used to offer the functionality one package provides
are often private and defined there:

```ada
package Signal_Filter
is

   type Context is private;

   procedure Clear_Context (C : out Context)
   --  API for this thing here
```

Types that _can_ be declared in a package's private part or a
package's body should always be declared there. Of course only do this
if you don't duplicate anything.

### Special note on testing

Testing Ada/SPARK can sometimes be tricky if the required types are
too hidden; and/or if you want to have multiple implementations of a
body, e.g:

* `foo.ads` (the common interface)
* `linux/foo.adb` (the Linux implementation)
* `hurd/foo.adb` (the HURD implementation)
* `testing/foo.adb` (the test framework where you can control/simulate
  behaviour)

If your project looks like this then you will probably want to place
from `foo.ads` into e.g. `types-foo.ads` to make sure your test stubs
can use them without circular inheritance problems.

## Prefer enumeration types

Whenever you can, you should use an enumeration type. For example,
instead of:

```ada
type Weekday is range 0 .. 6;
```

You should definitely prefer:

```ada
type Weekday is (Monday, Tuesday, Wednesday, Thursday, Friday,
                 Saturday, Sunday);
```

If you need the specific values you can use a rep-clause. You should
avoid writing rep-clauses whenever possible.

This is especially tricky when porting, or interfacing with, a C
application. It is very tempting to "just do the same", but then you
lose a lot of the benefits of Ada.

> [!TIP]
> Relevant GNAT Check rules:
> [Integer_Types_As_Enum](https://docs.adacore.com/live/wave/lkql/html/gnatcheck_rm/generated/predefined_rules.html#integer-types-as-enum)

## Porting and binding

Let's consider the specific example of weekdays. In C we might have:

```c
typedef int weekday;

#define MONDAY 0
#define TUESDAY 1
#define WEDNESDAY 2
#define THURSDAY 3
#define FRIDAY 4
#define SATURDAY 5
#define SUNDAY 6

#define FIRST_WORKING_DAY 0
#define LAST_WORKING_DAY 4

void do_someting(weekday day);
```

Under no circumstance should the Ada version of this use an integer
and a bag of constants. The best port looks like this:

```ada
type Weekday is (Monday, Tuesday, Wednesday, Thursday, Friday,
                 Saturday, Sunday);
subtype Working_Day is Weekday range Monday .. Friday;

procedure Do_Something (Day : in Weekday);
```

If we need to interface with / bind to C we can add a rep clause to
Weekday to make sure it matches the C constants.

We can also create C versions of the types in bindings, e.g:

```ada
type C_Weekday is new Interfaces.C.int;

function To_C (Day : Weekday) return C_Weekday;

procedure To_SPARK (C_Day   : in     C_Weekday;
                    Day     :    out Weekday;
                    Success :    out Boolean);
```

Note that when converting from C to Ada/SPARK we can't just assume the
C works -- we need to range check these values and deal with any
errors.

## Use of modular types

Modular types should be avoided unless you:
* specifically require wrap-around behaviour
* just want N bits of opaque data (e.g. type `Byte` for an opaque buffer)
* want to do bit-wise operations (e.g. `xor`)

Note that wanting to do left- and right-shift is not good enough; just
use `* 2` and `/ 2`, the compiler will optimise.

Specifically when porting a C program you should not convert unsigned
types blindly into modular types. For example if the C has:

```c
send_potatoes(unsigned int size);
delete_messages(unsigned int size);
```

Then the Ada/SPARK should probably look like this:

```ada
type Size_T is range 0 .. 2 ** 32 - 1;

procedure Send_Potatoes (Size : in Size_T);
procedure Delete_Messages (Size : in Size_T);
```

Or even better:

```ada
type Potato_Count is range 0 .. 2 ** 32 - 1;
--  Remember: overly generic types are bad. We're counting
--  something specific, in this case potatoes. Other C functions
--  that count other things should use other types.

type Message_Count is range 0 .. 5000;

procedure Send_Potatoes (Size : in Potato_Count);
procedure Delete_Messages (Size : in Message_Count);
```

This type might be bigger or smaller than the equivalent C type, but
this doesn't matter. You can (and should) deal with this in the
binding. Do not create modular types unless you actually need bit-wise
operations.

> [!TIP]
> There is a
> [GNAT extension](https://docs.adacore.com/live/wave/gnat_rm/html/gnat_rm/gnat_rm/gnat_language_extensions.html#unsigned-base-range-aspect)
> that will allow you to make "unsigned" base types. If you require
> exactly 32-bits for a unsigned 32 value, then this is what you should
> use.

## Avoid access types (i.e. pointers)

Whenever possible, avoid the use of access types. Array types and
implicit references cover most of the use-cases.

# Sanity checking representation

When interfacing with C, you often need to create record types in
SPARK that should perfectly match their C counterpart.

You can do this with a rep-clause, e.g:

```ada
   type Time_Interval is record
      Time_Start : Time_Spec;
      Time_End   : Time_Spec;
   end record
   with Convention => C,
        Size       => 384;
   --  Note the corresponding C struct has padding and legacy
   --  fields, which we remove in our SPARK world

   for Time_Interval use record
      Time_Start  at 0  range 0 .. 127;
      Time_End    at 16 range 0 .. 127;
   end record;
```

To make sure the rep-clause doesn't bit-rot away, you can create a
simple C file that you compile with your project:

```c
#include <the-relevant-headers.h>

/* struct time_interval_t */
_Static_assert(offsetof(struct time_interval_t, time_start) == 0,
               "Fix binding in package Types.C");
_Static_assert(offsetof(struct time_interval_t, time_end) == 16,
               "Fix binding in package Types.C");
_Static_assert(sizeof(struct time_interval_t) == 384,
               "Fix binding in package Types.C");
```

You can easily recognise the magic numbers from the representation
clauses; and we double check them to the actual values for the actual
struct in the C. If somebody changes either the Ada/SPARK or the C,
then this file has a chance to catch the problem.

> [!NOTE]
> Right now this is manual work, but we are working on a little tool
> that will generate this kind of C file automatically.

# Technical considerations

The above notes are about good style. There are some tricky
implementation details within SPARK that may influence type design.

The proof back-end of SPARK models types very differently:

| Ada                  | SMTLIB                                              |
|----------------------|-----------------------------------------------------|
| range types          | Int                                                 |
| modular types        | Bit-vectors                                         |
| floating point types | FloatingPoint (usually a Bit-vector under the hood) |
| fixed point types    | (Special modelling)                                 |

For practical reasons you specifically should avoid converting between
integer types and bit-vector types. Your program can contain both
without problem, it's specifically the _conversion_ between the two
that is problematic (for proof performance / decidability).

So for example, having an array indexed by a range type of floats is
fine. Comparing a range type to a modular type is not.

Note that it is possible to do this, but every time you do it, it
makes the problem for the SMT solvers worse and at some point you will
just get weird unpredictable behaviour.

Specifically, if you port from C and you translate normal integers as
integers and unsigned integers as modular types, then you will suffer
greatly.

There are some special annotations in SPARK that can be put on the
modular types to avoid some of these problems:

* [No_Bitwise_Operations](https://docs.adacore.com/spark2014-docs/html/ug/en/appendix/additional_annotate_pragmas.html#annotation-for-handling-modular-types-as-integers-in-all-provers)
* [No_Wrap_Around](https://docs.adacore.com/spark2014-docs/html/ug/en/appendix/additional_annotate_pragmas.html#annotation-for-overflow-checking-on-modular-types)

Note that you could read the above table as "if I want use floats I
could make all my integers into modular types to avoid theory
conversions"; but this is also a bad idea. Don't do it. SPARK is
designed to keep most of the integers in the `Int` theory; you need
this if you want to use `-gnato13 -gnatp` as is the recommended way of
compiling SPARK code.
