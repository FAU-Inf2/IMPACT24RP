#!/usr/bin/env bash

items=(adept_* poly_*)

for i in "${items[@]}"; do
    (
        cd "$i" || exit 1
        echo RUN HLS FOR "$i"
        tsp make -f driver.mk hls
    )
done
