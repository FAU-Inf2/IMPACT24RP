#!/usr/bin/env bash

AL=16
BS_1D="1024"
BS_2D="16,16"
BS_3D="32,32,32"


declare -A scops=(
	[adept_2d5p.py]="$BS_2D"
)

declare -A driver=(
	[adept_2d5p.py]="driver_2d.mk"
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

    polysage -S "$scop" -G -C orka -P axi -A "$al" -O tlf \
             --block-sizes "$bs" -W --tile-dims "i,j" --elem-dims "j,i" || exit 1
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
