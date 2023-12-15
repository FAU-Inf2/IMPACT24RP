#!/usr/bin/env bash

./aggregate.py -b \
	adept_2d5p,adept_2d9p,adept_3d19p,adept_3d27p,poly_jacobi_1d,poly_jacobi_2d,poly_heat_3d,poly_fdtd0,poly_fdtd1,poly_fdtd2  \
	-L 2d5p,2d9p,3d19p,3d27p,jac1d,jac2d,heat3d,fdtd0,fdtd1,fdtd2 \
	-Bs opt_al4_defaultBS

./aggregate.py -b \
	adept_2d5p,adept_2d9p,adept_3d19p,adept_3d27p,poly_jacobi_1d,poly_jacobi_2d,poly_heat_3d,poly_fdtd0,poly_fdtd1,poly_fdtd2  \
	-L 2d5p,2d9p,3d19p,3d27p,jac1d,jac2d,heat3d,fdtd0,fdtd1,fdtd2 \
	-Bs opt_al8_defaultBS
