OPENMP_INPUT = input.cpp tlf.cpp tlf_normal.cpp
OPENMP_INCLUDE = $(PWD)/
ORKAFLAGS = --log="Orka(DEBUG)" --vitis-max-widen-bitwidth 128 \
	--vitis-max-align 16 -I/opt/Xilinx/Vitis_HLS/2021.2/include/ \
	--cosim-argv "16384 1" --default-maxi-depth 512 \
	-DPOLYSAGE=1

HOST_BINARY_FLAGS = 4096 1
include /opt/orka/share/common.mk
# --vitis-max-align 16
