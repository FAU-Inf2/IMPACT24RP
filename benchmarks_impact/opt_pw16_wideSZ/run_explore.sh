#!/usr/bin/env bash

tapasco  --parallel --compositionDir "." --kernelDir "." --coreDir "." \
    explore [ tlf x 1 ] in frequency --basePath "." -p vcu118 --batchSize 5
