#!/usr/bin/env bash

bench="$1"

sets=(opt_al{4,8,16}_{default,half,wide}BS)

for s in "${sets[@]}"; do
    echo -n $s ", "
    ./aggregate.py -Bs $s -T -b "$bench"
done
