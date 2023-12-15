#!/usr/bin/env bash

AL=16
BS_1D="1024"
BS_2D="128,128"
BS_3D="64,64,64"




declare -A scops=(
	[poly_jacobi_1d.py]="$BS_1D"
	[adept_axpy.py]="$BS_1D"
	[adept_scalar_mult.py]="$BS_1D"
	[adept_2d5p.py]="$BS_2D"
	[adept_2d9p.py]="$BS_2D"
	[poly_fdtd0.py]="$BS_2D"
	[poly_fdtd1.py]="$BS_2D"
	[poly_fdtd2.py]="$BS_2D"
	[poly_jacobi_2d.py]="$BS_2D"
	[adept_3d19p.py]="$BS_3D"
	[adept_3d27p.py]="$BS_3D"
	[poly_heat_3d.py]="$BS_3D"
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
