# Benchmark Notes

Each subdirectory contains one directory
per benchmark code. Each of these contains
four relevant files. The `input.cpp` is the test
driver that generates the test data,
offloads the function `tlf` (the
optimized version, defined in `tlf.cpp`)
to the FPGA and checks it's results
agains the results that
the host function `tlf_normal` (defined
in `tlf_normal.cpp`).
Finally, the timings of the FPGA runtimes
are recorded in the `timing*.json` files.

Note that you can use `driver.mk` with
the command `make -f driver.mk hostBinary`
and `make -f driver.mk bitstream` in the
ORKA Docker container to generate the host
and the FPGA portion of the program.

To generate the benchmark sets, we used
the helper scripts `generate.sh`. The
shell function `generate` contains
the three necessary calls to polysage.
The command line flags are described
in `../code_generator/README.md`.

The test drivers `input.cpp` use a custom
memory allocator (as defined in
`#include "orka_mem_alloc.hpp"`) to prepare
the memory region that ORKA-HPC ships to the
FPGA during offloading. It makes sure, that
the memory region is big enough even after
the iteration padding, that the polysage applies.
The header lives in the
ORKA-HPC [compiler](https://cs2-gitlab.cs.fau.de/orka/compiler)
repo, but it is also included for convenience under
`misc/orka_mem_alloc.hpp`.

