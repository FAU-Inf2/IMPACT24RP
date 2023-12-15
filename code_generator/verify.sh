#!/usr/bin/env bash

kernels=(adept2d5p adept3d2p)

rm -f code_*.{c,h}
rm -f verify_*

./run.sh

for i in "${kernels[@]}"; do
	make verify_$i
	./verify_$i
done

