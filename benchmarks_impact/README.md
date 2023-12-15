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
