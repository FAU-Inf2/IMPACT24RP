#!/usr/bin/env bash

AL=8

declare -A scops=(
	[poly_jacobi_1d.py]="512"
	[adept_axpy.py]="512"
	[adept_scalar_mult.py]="512"
	[adept_2d5p.py]="64,64"
	[adept_2d9p.py]="64,64"
	[poly_fdtd0.py]="64,64"
	[poly_fdtd1.py]="64,64"
	[poly_fdtd2.py]="64,64"
	[poly_jacobi_2d.py]="64,64"
	[adept_3d19p.py]="32,32,32"
	[adept_3d27p.py]="32,32,32"
	[poly_heat_3d.py]="32,32,32"
)

declare -A driver=(
	[poly_jacobi_1d.py]="driver_1d.mk"
	[adept_axpy.py]="driver_1d.mk"
	[adept_scalar_mult.py]="driver_1d.mk"
	[adept_2d5p.py]="driver_2d.mk"
	[adept_2d9p.py]="driver_2d.mk"
	[poly_fdtd0.py]="driver_2d.mk"
	[poly_fdtd1.py]="driver_2d.mk"
	[poly_fdtd2.py]="driver_2d.mk"
	[poly_jacobi_2d.py]="driver_2d.mk"
	[adept_3d19p.py]="driver_3d.mk"
	[adept_3d27p.py]="driver_3d.mk"
	[poly_heat_3d.py]="driver_3d.mk"
)

# $1: scop
# $2: al
# $3: blocksizes
function generate() {
    al="$2"
    bs="$3"
    scop="$HOME/polysage/scops/$1"

    drv="${driver[$1]}"

    cp $HOME/synthBin/benchmarks_impact/clang_format .clang-format
    cp $HOME/synthBin/benchmarks_impact/"$drv" driver.mk

    polysage -S "$scop" -D -G -C orka -P axi -A "$al" -O tlf --block-sizes "$bs" || exit 1
    polysage -S "$scop" -D -G -C normal -P lin -O tlf_normal || exit 1
    polysage -S "$scop" -I -A "$al" -P axi || exit 1
}


for i in "${!scops[@]}"; do
	mkdir -p "${i//.py}"
	(
	    cd "${i//.py}" || exit 1
	    generate "$i" $AL "${scops[$i]}"
	)
done
