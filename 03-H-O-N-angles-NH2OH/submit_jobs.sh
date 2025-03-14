#!/usr/bin/bash

find . -mindepth 3 -maxdepth 3 -type d | while read subdir; do
    (
        cd "$subdir" || exit

        /home/nhi/bin/lammps-29Aug2024/src/lmp_mpi -in lammps.in
    )
done
