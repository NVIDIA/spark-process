# Spark Process

This is the repository for the reST sources of the NVIDIA SPARK
Process. A pre-built version is [available
here](https://nvidia.github.io/spark-process/).

## Disclaimer

This document collection contains a reference process whose initial
version has been developed jointly between NVIDIA and AdaCore, then
reviewed by TÜV-SÜD. It is not meant to represent the current stage of
the NVIDIA or AdaCore internal development and certification
processes, nor does it guarantee TÜV-SÜD acceptance or
endorsement. Adjustments and edits made past this initial version may
be applied over time to reflect evolution of the technology, state of
the art, or feedback, and may not receive systematic review from all
the initial authors.

## Roadmap

Several sections and checklists of the process have been identified to
be too heavy. We are working on significant streamlining.

## How to build

You can build the HTML or PDF document locally, this is especially
important if you want to contribute. This is what you need to get
started:

* Python3 (>= 3.10, but anything from this decade should work)
* GNU Make
* texlive-full (if you want to build the PDF)

Install the Python dependencies:

```bash
python3 -m pip install --upgrade -r requirements.txt
```

Then you can build the HTML like so:

```bash
make html
```

## Source organisation

* `pygments/` -- this contains syntax highlighting for SPARK
* `util/` -- this contains various document generation scripts
* `source/process/` -- this is where the main document tree lives,
  start at index.rst
* `source/process/process/` -- this is where the actual process
  document lives
* `source/process/checklist/` -- this is where the TRLC files live
  that generate the checklist
* `source/process/tracing/spark_assumptions/` -- this is where the
  TRLC files live that generate the assumption tracing chapter
* `source/process/tracing/iso_26262/` -- this is where iso tracing
  lives

A large part of the process is generated from TRLC files. TRLC is a
[language](https://bmw-software-engineering.github.io/trlc/lrm.html)
and [tool](https://github.com/bmw-software-engineering/trlc) for
expressing requirements with attached meta-data and policy.

* We're using it to easier validate the input, and allow simple Python
  scripts to generate `.rst` files from large sections of regular
  data.

* The data is easier to machine parse, and can so feed directly into
  other tools.

## Copyright & License

Unless noted otherwise, all material is:

* (C) Copyright (C) 2024 - 2025 NVIDIA CORPORATION & AFFILIATES
* (C) Copyright (C) 2021 - 2024 AdaCore

The pygments parser is taken from the [SPARK 2014
repository](https://github.com/AdaCore/spark2014/blob/master/docs/sphinx_support/ada_pygments.py),
please refer to that repository for licensing information.

The material quoted from ISO 26262 is:

* (C) ISO. This material is reproduced from ISO 26262, with permission of
  the American National Standards Institute (ANSI) on behalf of the
  International Organization for Standardization. All rights reserved.

The process document is licensed under the [GFDL
v1.3](https://www.gnu.org/licenses/fdl-1.3.en.html#license-text).

Any supporting tools and scripts are licensed under the [GPL
v3](https://www.gnu.org/licenses/gpl-3.0.html#license-text).

## Acknowledgements

We would like to thank the following people for their contributions to
this process (in lexicographic order):

* Brian Gaeke (NVIDIA)
* Dan Hettena (NVIDIA)
* Dmitry Kulagin (NVIDIA)
* Duane McInerney (NVIDIA)
* Erwan Le Guillou (AdaCore)
* Florian Schanda (NVIDIA)
* Vasiliy Fofanov (AdaCore)
* Yannick Moy (AdaCore)
