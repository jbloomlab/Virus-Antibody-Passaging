# Viral Antibody Passaging

This repository contains a pipeline for identifying antibody escape mutations in viruses passaged with antibodies. The pipeline is agnostic to the virus. The sequencing data must be Illumina, paired-end, and not amplified with virus-specific primers. Additionally, sequencing runs must be provided for the viral 'Stock'.

Currently, the pipeline is running with data from HMPV and RSV-A. Experiments were performed by Evelyn Harris in the [Boonyaratanakornkit lab](https://research.fredhutch.org/boonyaratanakornkit/en.html).

## Getting Started

Clone the pipeline from GitHub.

```bash
git clone https://github.com/jbloomlab/Virus-Antibody-Passaging.git
cd Virus-Antibody-Passaging
```

Install the required software using `conda` or `mamba`. If you don't have either of these installed, follow the instructions [here](https://docs.anaconda.com/miniconda/miniconda-install/) to install them.

```bash
conda env create --file environment.yml
conda activate antibody-passaging
```

**Note, this pipeline is specifically configured for Fred Hutch Cancer Center's `rhino` server. It's possible to run on other platforms, but not tested for them.**

## Configuring the Pipeline

Edit the [`samples.csv`](/configuration/samples.csv) file in the [`configuration`](/configuration/) directory with your samples. For example, here's the first row of `samples.csv`:

| Virus |  Run  | R1                                    | R2                                    |
|-------|-------|---------------------------------------|---------------------------------------|
| RSV-A | Stock | /path/to/run/samples_R1.fastq.gz      | /path/to/run/samples_R2.fastq.gz      |


There are four columns in the `samples.csv` table.

1. **Virus**: The name of the virus you're sequencing.
2. **Run**: The name of the condition (Stock, Untreated, Antibody-1, ect...).
3. **R1**: The absolute path to the R1 sequencing run.
4. **R2**: The absolute path to the R2 sequencing run.

**Note, there must be at least one entry for `Stock` for each `Virus`. Otherwise, you won't be able to make a Stock consensus sequence to align the remaining conditions to.**

After you've added an entry for each of your samples, you need to edit the `pipeline.yml` configuration file. This file is in YAML format ([check out this reference](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html) if you're unfamiliar). 

You'll need to update [`pipeline.yml`](/configuration/pipeline.yml) with a `fasta` reference and `gff` file for each virus in `samples.csv`. Make sure the name in `pipeline.yml` is the same as the name in `samples.csv`.

```yaml
#### ------------------------- Genomes ------------------------ ####

RSV-A:
  ref: configuration/reference/KT992094_truncated.fasta
  gff: configuration/reference/KT992094_truncated.gff

#### ------------------------- Params ------------------------ ####
```

Finally, add the corresponding `ref` and `gff` files to your pipeline. It doesn't matter where you put them as long as the path is correct in `pipeline.yml`. However, I'd recommend adhering to the current structure (`/configuration/reference/`).

## Running the Pipeline

The pipeline is written in `snakemake` and run as such. First, check that everything looks correct with a 'dry-run' (nothing is actually run).

```bash
snakemake --dry-run
```

If you get an error at this point, there's likely a problem with the configuration. If you don't get an error, run the pipeline by submitting it to `slurm`.

```bash
sbatch run_analysis.bash
```

## Interpreting the Results

After the pipeline runs, the results will be deposited in [`results/`](/results/). This folder contains all of the intermediate data including alignments for each sample and virus. The main figures summarizing the depth and variants for each sample are organized by virus and are located in [`results/summary/<virus>`](/results/summary/RSV-A/).
