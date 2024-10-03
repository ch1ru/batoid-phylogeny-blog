# prep_data.py

import argparse
from typing import List
import pandas as pd
import numpy as np
import subprocess
from Bio.Nexus import Nexus
from Bio import SeqIO
import os

def fetch_datasets(gene_table: pd.DataFrame):
    unaligned_files= []
    for column in gene_table.columns:
        if column == "species":
            continue
        print(f"Collecting {gene_table[column].size} Genbank sequences of gene {column}...")
        fasta_file = f"{column}.fasta"
        cmd = ["ncbi-acc-download", "--out", fasta_file, "--format", "fasta", f"{''.join(str(acc) + ' ' for acc in gene_table[column])}"]
        if os.path.exists(fasta_file):
            if input(f"{fasta_file} already exists, overwrite? [y/N] ") == "y":
                subprocess.call(cmd)
        else:
            subprocess.run(cmd)
            
        unaligned_files.append(fasta_file)
    
    return unaligned_files

def modify_id(df: pd.DataFrame):
    for column in df.columns:

        fasta_file = f"{column}.fasta"
        if column == "species":
            species = df[column].values
            continue

        for s in species:

            with open(fasta_file, 'r') as file:
                filedata = file.read()

            # Replace the target string
            filedata = filedata.replace(f">{df[df['species'] == s][column].values[0].lstrip()}", f">{s} ")
            # Write the file out again
            with open(fasta_file, 'w') as file:
                file.write(filedata)

        # validate seqs
        records = [record.id for record in SeqIO.parse(fasta_file, "fasta")]
        for i, record in enumerate(records):
            if record.lstrip() != df["species"][i].lstrip():
                raise Exception("Sequences requested don't match sequences downloaded.")
            
def align_sequences(unaligned_files: List[str]):
    aligned_files = []
    for file in unaligned_files:
        outfile = f"{file.split('.')[0]}.nex"
        cmd = ["clustalw", "-type=dna", f"-infile={file}", "-output=nexus", f"-outfile={outfile}", "-outorder=input"]
        if os.path.exists(outfile):
            if input(f"{outfile} already exists, overwrite? [y/N] ") == "y": # if exists, ask user if they want to replace it
                subprocess.run(cmd)
        
        else: # no alignments exist, proceed with multiple alignment
            subprocess.run(cmd)
        
        aligned_files.append(outfile)

    return aligned_files

def concat_nexus(aligned_files: List[str], output_name: str):
    nexi = [(fname, Nexus.Nexus(fname)) for fname in aligned_files]

    combined = Nexus.combine(nexi)
    allowed_exts = ["nex", "nxs", "nexus"]
    output_name = f"{output_name}.nex" if not any(x in output_name for x in allowed_exts) else output_name
    combined.write_nexus_data(filename=open(output_name, "w"))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='Script for phylogenetic analysis.',
        description='Fetches sequences data, aligns sequences, concatenates into nexus partition file.',
        epilog='See the blog at'
    )

    parser.add_argument('-o', '--output') 
    parser.add_argument('-i', '--input')

    args = parser.parse_args()

    df = pd.read_csv(args.input)

    unaligned_files = fetch_datasets(gene_table=df)
    modify_id(df)
    aligned_files = align_sequences(unaligned_files)
    concat_nexus(aligned_files, output_name=args.output)
