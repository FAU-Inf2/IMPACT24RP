# README

## Prerequisites

Our code generator is written in Python 3.8 and
must run in an environment that provides the
following:

- The ISL Library (with python bindings)
- The Barvinok Library (with python bindings)
- Python 3.8
- The following Python libraries: {igraph, parsita, graphviz}
- PET to derive SCoPs.

The Docker container of the
[ORKA-HPC environment](https://cs2-gitlab.cs.fau.de/orka/orkadistro)
contains the prerequisites above necessary to run
the code generator.
Vou can also install them under
Ubuntu 18.04 manually if you wish.

To install the necessary Python
version and packages you have to use:
- $ apt-get install python3.8 python3.8-dev python3-pip
- $ python3.8 -m pip install && MAKEFLAGS="-j" python3.8 -m pip install igraph
- $ python3.8 -m pip install parsita
- $ python3.8 -m pip install graphviz
The ISL library and ISL python bindings
cannot be installed from `https://repo.or.cz/isl.git`
directly, as we modified the ISL sources. Our fork is
available at `https://cs2-gitlab.cs.fau.de/orka/isl`
and, alternatively, via the patch `misc/isl.patch`.
Our changes to ISL export some (previously unexported)
functions to be exported as python bindings.
For Barvinok, just follow the instructions
in `https://repo.or.cz/barvinok.git`. Note that it
might necessary to install the modified ISL first and
then let Barvinok's build system link agains that version
of ISL. Please make sure, that Barvinok and ISL are
installed at `/usr/lib`.

## Usage

Polysage parses the following command line flags.

- `-S <scopfile>`: The Scop file. See `scops` for examples.
- `-h`: Print a list of the available flags.
- `-I`: Generate a testbench file.
- `-O`: Set the file name that hold the transformed code.
- `-Bu <num>`: Use `<num>` uniformly as tile sizes in all dimensions.
- `-Bs <numlist>`: Use the values in `<numlist>` for each tiling dimensions.
- `-G`: Causes code to emit.
- `-C {orka, normal}`: `normal` will emit the original loop nest
  represented by `<scopfile>`. `orka` will emit the optimized loop nest.
- `-A <powOfTwo>`: Set the port width.

Note that this list is not exhaustive. There
are more flags for debugging purposes.

## Offloading the generated code to the FPGA

To synthesize and offload the code that polysage
generates, we employ the [ORKA-HPC environment](https://cs2-gitlab.cs.fau.de/orka/orkadistro).
which provides a Docker environment with the ORKA-HPC
compiler running in it. ORKA-HPC implements a subset of
OpenMP and can offload OpenMP target regions to FPGAs.

## Further notes

The upstream repo of this code generator lives
at `https://cs2-gitlab.cs.fau.de/orka/polysage`.
