!pip install Bio
!pip install logomaker
!pip install pymsaviz

import pandas as pd
import sys
import os
import time
import argparse
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline 
plt.ion()

import logomaker as lm

from collections import Counter,defaultdict
from numpy import log
from Bio import AlignIO
from Bio import PDB

import numpy as np  # Import numpy for initialization

#Insert aligned fasta sequence

align = AlignIO.read("c:\\Users\\yourlocation", "fasta")

from pymsaviz import MsaViz, get_msa_testdata
msa_file = open('Yourfile.fas')

def frequency(align):
    # Create an empty DataFrame with columns for amino acids
    amino_acids = ['-']
    df = pd.DataFrame(columns=amino_acids, data=np.zeros((len(align[0]), len(amino_acids))))

    # Iterate through the alignment and count amino acids at each position
    for a in range(len(align[0])):
        for x in align[:, a]:
            if x in amino_acids:
                df.at[a, x] += 1
            else:
                # Add new amino acid to the DataFrame
                amino_acids.append(x)
                df[x] = 0
                df.at[a, x] = 1
    
    #changes the index in order that the first aa is actually 1
    df.index = df.index + 1

    return df

# Example usage (assuming 'align' is a valid MSA)
frequency_table = frequency(align)
frequency_table_2 = frequency(align)
# Iterate through each row to find the most frequent amino acid and its frequency percentage
most_frequent_amino_acids = []
identity = []

for index, row in frequency_table.iterrows():
    most_frequent_amino_acid = row.idxmax()
    most_frequent_count = row.max()
    total_count = row.sum()
    
    if most_frequent_amino_acid == "-":
        identity_percentage = 0
    else:
        identity_percentage = (most_frequent_count / total_count) * 100

    
        
    most_frequent_amino_acids.append(most_frequent_amino_acid)
    identity.append(identity_percentage)
    
# Add new columns for the most frequent amino acid and its frequency percentage
frequency_table['MostFrequentAminoAcid'] = most_frequent_amino_acids
frequency_table['FrequencyPercentage'] = identity

print(frequency_table)

# Load the PDB file
# NOTE: the PDB sequence has to have the same lenght of the aligment

parser = PDB.PDBParser(QUIET=True)
structure = parser.get_structure("my_protein", "c:\\Users\\Filippo\\Desktop\\BioinformaticsPmmo\\3rgb666.pdb")
# Add frequency values as bf records

#Iterate through the structure and assign frequency values
i = 0  # Initialize the frequency index
for model in structure:
    for chain in model:
        for residue in chain:
            # Set the full identifier for the residue
            residue.full_id = (' ', chain.id, ' ', (' ', residue.id[1], ' '))
            # Set the B-factor as a representation of frequency
            for atom in residue:
                atom.set_bfactor(identity[i])
            i += 1

# Save the modified structure to a new PDB file
io = PDB.PDBIO()
io.set_structure(structure)
io.save("c:\\Users\\modified_color.pdb")


mv = MsaViz(msa_file, wrap_length=60, show_grid=True, show_consensus=True)
fig = mv.plotfig()
