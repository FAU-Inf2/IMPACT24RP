#!/usr/bin/env bash

items=(adept_* poly_*)

for i in "${items[@]}"; do
    (
        cd "$i" || exit 1
        echo RUN BENCHMARKS FOR "$i"
        make -f driver.mk benchmark || exit 1

        make -f driver.mk runAndGet || exit 1
        make -f driver.mk runAndGet || exit 1
        make -f driver.mk runAndGet || exit 1
        make -f driver.mk runAndGet || exit 1
    )
done
