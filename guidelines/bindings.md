<!--
SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION &
                        AFFILIATES. All rights reserved.
-->

# Bindings guidlines

Creating good bindings is an _art_, and can be __the most tricky
part__ of creating a SPARK program. These guidelines document some
common approaches and best practice.

In a C - SPARK binding there are generally two parts (which can
sometimes be combined into one):

* A thin binding that makes the C API available in Ada (or exports a
  Ada subprogram to C)
* A thick binding that makes the API more "sparky"

The most important document to read and understand is [Appendix
B.3](https://docs.adacore.com/R/docs/gnat-24.2/arm22/html/arm22/RM-B-3.html)
of the Ada RM. Understanding it is a must, most importantly it lays
out the options you have when choosing parameter modes.

The primary game you will be playing is:

* Hide the pointers
* Identify global data and side effects
* Identify constraints

## Thin bindings

You can make a good start by using the gcc option `gcc -fdump-ada-spec
file.c`. This creates a package hierarchy that with Ada declarations
that allow you to call C functions.

Do not use this as is - it is not recommended to e.g. make this part
of your build. You will want to modify the generated code to make it
more sane, e.g. trimming out the parts you don't need, cleaning up
types, removing access types in favour of `in out` parameters, etc.

The code generated is not always correct. If your C uses one of these
constructs you need to manually check:

* packed structs -- you will need to write a rep clause
* macros -- you might need to create a wrapper c function which you
  then bind to, of particular difficulty are variadic macros
* variadic functions

### Example

Consider this sample C file:

```c
typedef struct {
  int x;
  int y;
} potato;

void do_something(potato *p);
```

Compiling with `-fdump-ada-spec` will produce:

```ada
package foo_c is

   type potato is record
      x : aliased int;  -- foo.c:2
      y : aliased int;  -- foo.c:3
   end record
   with Convention => C_Pass_By_Copy;  -- foo.c:4

   procedure do_something (p : access potato)  -- foo.c:6
   with Import => True,
        Convention => C,
        External_Name => "do_something";

end foo_c;
```

This is fine, in a way. But you should probably change several things
here:

* Making the names a bit more Ada
* Removing the access type

```ada
package foo_c is

   type C_Potato is record
      x : aliased int;  -- foo.c:2
      y : aliased int;  -- foo.c:3
   end record
   with Convention => C_Pass_By_Copy;  -- foo.c:4

   procedure C_Do_Something (P : in out C_Potato)  -- foo.c:6
   with Import => True,
        Convention => C,
        External_Name => "do_something";

end foo_c;
```

It might also be worth adding a
[global](https://docs.adacore.com/spark2014-docs/html/ug/en/source/subprogram_contracts.html#data-dependencies)
and [termination
contract](https://docs.adacore.com/spark2014-docs/html/ug/en/source/subprogram_contracts.html#contracts-for-termination),
if you're sure about it. Perhaps:

```ada
package foo_c is

   type C_Potato is record
      x : aliased int;  -- foo.c:2
      y : aliased int;  -- foo.c:3
   end record
   with Convention => C_Pass_By_Copy;  -- foo.c:4

   procedure C_Do_Something (P : in out C_Potato)  -- foo.c:6
   with Import => True,
        Convention => C,
        External_Name => "do_something",
        Global => null,
        Always_Terminates;

end foo_c;
```

Note that you will need to read and understand the API documentation
of the C function you're binding to, or even better read and
understand the source code (if you have it).

Also note that most likely your thin binding won't be usable in SPARK
directly, you will most likely need to create a thick binding.

## Thick bindings

A thick binding is usually a simple procedure that converts between a
SPARK API and the C API. You do this to:

* Hide pointers
* Make side effects explicit
* Perform data validation
* Add contracts to model behaviour
* Deal with arrays

### Example

Consider the following C API:

```c
#include <stddef.h>

int flash_rom(char *data, size_t n);
// returns 0 on success
```

First we create the thin binding with `-fdump-ada-spec`:

```ada
package foo_c is

   function flash_rom (data : Interfaces.C.Strings.chars_ptr; n : stddef_h.size_t) return int  -- foo.c:3
   with Import => True,
        Convention => C,
        External_Name => "flash_rom";

end foo_c;
```

In this example we don't really have a string, we just have some
opaque data and a number of bytes to write. We could change the
signature like so, while still complying to Appendix B.3:

```ada
package foo_c
with SPARK_Mode => Off
is

   function C_Flash_ROM (Data : System.Address; N : Interfaces.C.size_t)
                        return Interfaces.C.int
   with Import => True,
        Convention => C,
        External_Name => "flash_rom";

end foo_c;
```

We're also adding `SPARK_Mode => Off` here to make sure this not used
from SPARK code.

Next we can sketch the thick binding:

```ada
package ROM_Interface
with SPARK_Mode
is

   type Byte is mod 256;
   type ROM_Image is array (Positive range <>) of Byte;

   procedure Flash_ROM (Image   : in     ROM_Image;
                        Success :    out Boolean);

end ROM_Interface;
```

Note that normally you'd not define the types here but in a more
central place, but for the purpose of this example it's fine.

There are several changes made here:

* We don't have a function anymore, we have a procedure that returns a
  success flag. Since the original documentation didn't describe
  anything other than 0 or non-zero using a `Boolean` here is
  fine. Otherwise you could create some kind of enum type to capture
  all errors.

* We also don't have a pointer + size, we have a real array we provide
  here.

However this is not quite right yet. There are some implicit
pre-conditions and side-effects (the flashing of the rom) that we
should model. So we amend our spec like this:

```ada
package ROM_Interface
with SPARK_Mode,
     Abstract_State => The_ROM
is

   type Byte is mod 256;

   type ROM_Image is array (Positive range <>) of Byte
   with Predicate => ROM_Image'Length > 0;

   procedure Flash_ROM (Image   : in     ROM_Image;
                        Success :    out Boolean)
   with Global => (Output => The_ROM);

end ROM_Interface;
```

We're adding a pre-condition to all instances of ROM_Image to rule out
empty images, and we're also explicitly introducing state to model the
effect on the hardware.

The package body is `SPARK_Mode => Off` and just calls the C function:

```ada
with Interfaces;   use Interfaces;
with Interfaces.C; use Interfaces.C;

with foo_c;        use foo_c;

package body ROM_Interface
with SPARK_Mode => Off
is

   procedure Flash_ROM (Image   : in     ROM_Image;
                        Success :    out Boolean)
   is
      Status : Interfaces.C.int;
   begin
      Status  := C_Flash_ROM (Data => Image'Address,
                              N    => Image'Length);
      Success := Status = 0;
   end Flash_ROM;

end ROM_Interface;
```

## Data validation

Often you will find that the C API uses `int` everywhere, and if
you're really lucky you might find an `enum`. However note that in C
an `enum` is just an `int`, and it is perfectly legal to assign values
to it that are not one of the enumerated values.

If you C function looks like this:

```c
typedef enum {OK, FAIL, FILE_NOT_FOUND} status_t;

status_t do_something();
```

Then your Ada thin binding interface might look like this:

```ada
type C_Status_T is (Ok, Fail, File_Not_Found);

function C_Do_Something return C_Status_T
with Import,
     Convention_C,
     External_Name => "do_something";
```

But your thick binding needs to take care of the invalid values. You
could either do this:

```ada
type Status_T is (Ok, Fail, File_Not_Found, Data_Validation);

procedure Do_Something (Status : out Status_T)
with Global => (In_Out => Something);
```

Or perhaps you don't even care about the other errors, in which case
you could do:

```ada
procedure Do_Something (Success : out Boolean)
with Global => (In_Out => Something);
```

Or you could model the error explicitly:

```ada
procedure Do_Something (Status                : out C_Status_T;
                        Data_Validation_Error : out Boolean);
with Global => (In_Out => Something);
```

You have many options, try to pick one that works best for your
intended use of this function inside your SPARK program.

## Hiding pointers

You should try your best to hide away pointers. In order of preference
you should:

* Convert address + size into an (unconstrained) array
* Convert reference-style parameters into normal Ada parameters
* Hide the access type behind a limited private type
* Hide the access type behind a private type, ideally with [ownership
  annotations](https://docs.adacore.com/spark2014-docs/html/ug/en/appendix/additional_annotate_pragmas.html#annotation-for-enforcing-ownership-checking-on-a-private-type)
* Expose the access type or use `System.Address`.

## Ignored parameters

With some C APIs you can have a single function with multiple modes of
operation, where some parameters are ignored based on how it is used.

In SPARK you should provide multiple procedures for this, one for each
mode of operation. The thick binding should then deal with the
details.

A silly example could be this:

```c
int write_rom(int default_image, char *data, size_t n);
// Write the image. If default_image is 1 we write the factory default
// image and data and size are ignored. If default_image is 0 we write
// n bytes pointed to by data to the device.
```

The thin binding has just one function. However the SPARK API should
provide two procedures, instead of one:

```ada
procedure Write_Factory_Default
with Global => (Output => The_ROM);

procedure Write_Custom_Image (Image : in ROM_Image)
with Global => (Output => The_ROM);
```

In the thick binding we then supply suitable constants or null values
for the thin binding.

## Inline thin binding

It is generally recommended to have a separate thin and thick
binding. However if you do not expect your API to change often
(e.g. you're binding to a well established POSIX API) then it can be a
good idea to combine the two into one. For example with our
ROM_Interface example we could instead write the body like this:

```ada
with Interfaces;   use Interfaces;
with Interfaces.C; use Interfaces.C;

package body ROM_Interface
with SPARK_Mode => Off
is

   procedure Flash_ROM (Image   : in     ROM_Image;
                        Success :    out Boolean)
   is
      function C_Flash_ROM (Data : System.Address; N : Interfaces.C.size_t)
                           return Interfaces.C.int
      with Import => True,
           Convention => C,
           External_Name => "flash_rom";

      Status : Interfaces.C.int;
   begin
      Status  := C_Flash_ROM (Data => Image'Address,
                              N    => Image'Length);
      Success := Status = 0;
   end Flash_ROM;

end ROM_Interface;
```

Ultimately this is a design choice, and either option is fine.

## Validating Contracts

Adding pre-conditions on your binding is always "safe". In fact, not
adding them might need lead to missed errors.

Adding post-conditions is more tricky. Since the body of the binding
is usually `SPARK_Mode => Off` SPARK will implicitly trust the
contract. Hence it is especially important to get them right.

If you have access to the C source, you might want to consider
analysing the called function with a model checker like CBMC. You can
create a harness that adds all your SPARK contracts as
`__CPROVER_assume`, and checks the post-conditions with
`__CPROVER_assert`.

For example we might have in SPARK:

```ada
procedure Add_One (N : in out Integer)
with Global => null,
     Pre => N < 1000,
     Post => N > N'Old;
```

And this is our C function that we bind to:

```c
int add_one(int input)
{
  return input + 1;
}
```

We can create a harness like so:

```c
#include "add_one.c"

extern int nondet_int();

void harness()
{
  int input = nondet_int();
  __CPROVER_assume(input < 1000);
  int output = add_one(input);
  __CPROVER_assert(output > input, "failed post");
}
```

And run CBMC on it:

```
cbmc harness.c --function harness

CBMC version 6.10.0 (cbmc-6.10.0-dirty) 64-bit x86_64 linux
Type-checking harness
Generating GOTO Program
Adding CPROVER library (x86_64)
Removal of function pointers and virtual functions
Generic Property Instrumentation
Starting Bounded Model Checking
Passing problem to propositional reduction
converting SSA
Running propositional reduction
SAT checker: instance is UNSATISFIABLE

** Results:
add_one.c function add_one
[add_one.overflow.1] line 3 arithmetic overflow on signed + in input + 1: SUCCESS

harness.c function harness
[harness.assertion.1] line 10 failed post: SUCCESS

** 0 of 2 failed (1 iterations)
VERIFICATION SUCCESSFUL
```

Obviously its important to accurately reflect the pre- and
post-conditions in the harness, and it might not be possible to do it
for all. However this approach can be used to gain additional
confidence on the correctness of your contracts on the thick binding.

Note that this approach can also catch missing pre-conditions on your
SPARK binding.

Finally note that you don't have to use CBMC here, you could also use
e.g. Frama-C/WP.
