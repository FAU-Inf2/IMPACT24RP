#!/usr/bin/env bash

scops=(adept_* poly_*)

for i in "${scops[@]}"; do
    (
        cd "$i" || exit 1
        make -f driver.mk runMock || exit 1
    )
done
