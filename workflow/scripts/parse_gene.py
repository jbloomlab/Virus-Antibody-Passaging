import requests
import gzip
import argparse as args
from io import BytesIO
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

def download_and_open_gzip(url):
    """
    Download a remote genome and unzip it.
    """
    response = requests.get(url)
    response.raise_for_status()
    return gzip.open(BytesIO(response.content), 'rt')

def parse_gene_from_genome(fasta_url, gff_url, gene_id, outpath):
    """
    Parse a gene from a genome using a gff and write to a fasta file.
    """

    # Download and open the genome
    fasta_file = download_and_open_gzip(fasta_url)
    genome = next(SeqIO.parse(fasta_file, "fasta"))
    fasta_file.close()

    # Download and extract coordinates from the gff
    gff_file = download_and_open_gzip(gff_url)
    protein_coordinates = None
    for line in gff_file:
        if line.startswith('#'):
            continue
        parts = line.strip().split('\t')
        if parts[2] == 'CDS' and f'gene={gene_id}' in parts[8]:
            protein_coordinates = parts
            break
    gff_file.close()
    if protein_coordinates is None:
        raise ValueError(f'Gene {gene_id} not found in genome')
    
    # Extract the gene from the genome
    start, end = int(protein_coordinates[3]) - 1, int(protein_coordinates[4])
    if protein_coordinates[6] == '+':
        protein_sequence = genome.seq[start:end]
    else:
        protein_sequence = genome.seq[start:end].reverse_complement()

    # Check that the sequence is a multiple of 3
    if len(protein_sequence) % 3 != 0:
        raise ValueError("Gene sequence is not a multiple of 3, are you sure it's a coding sequence?")
    # Check that the protein sequence starts with a start codon
    if protein_sequence[:3] != 'ATG':
        raise ValueError("Gene sequence does not start with a start codon, are you sure it's a coding sequence?")

    # Write the gene to a fasta file
    gene_record = SeqRecord(protein_sequence, id=gene_id, description='')
    with open(outpath, 'w') as out:
        SeqIO.write(gene_record, out, 'fasta')

if __name__ == '__main__':
    parser = args.ArgumentParser()
    parser.add_argument('fasta_url', help='URL of the genome fasta file')
    parser.add_argument('gff_url', help='URL of the gff file')
    parser.add_argument('gene_id', help='ID of the gene to extract')
    parser.add_argument('outpath', help='Path to write the gene to')
    args = parser.parse_args()
    parse_gene_from_genome(args.fasta_url, args.gff_url, args.gene_id, args.outpath)

    
    

    


