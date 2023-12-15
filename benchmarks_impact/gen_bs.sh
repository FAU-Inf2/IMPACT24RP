#!/usr/bin/env bash

items=(adept_* poly_*)

for i in "${items[@]}"; do
    (
        cd "$i" || exit 1
        tsp make -f driver.mk bitstream
    )
done
