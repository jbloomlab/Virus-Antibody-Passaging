#!/bin/bash
#
#SBATCH -c 8
#SBATCH --time 1-0
#SBATCH -J "{rule}"

# stop on errors
set -e

echo "Running snakemake..."

# Run the main analysis on `slurm` cluster
snakemake \
    --software-deployment-method conda \
    --conda-frontend mamba \
    --conda-prefix ./env \
    -j 999 \
    --latency-wait 60 \
    --rerun-incomplete
