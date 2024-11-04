#!/bin/bash
#
#SBATCH -c 1
#SBATCH --time 1-0

# stop on errors
set -e

echo "Running snakemake..."

# Run the main analysis on `slurm` cluster
snakemake \
    --software-deployment-method conda \
    --conda-frontend mamba \
    --conda-prefix ./env \
    --workflow-profile profiles \
    --rerun-incomplete
