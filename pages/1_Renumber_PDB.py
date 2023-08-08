import argparse
import subprocess
import streamlit as st
import os
import time
import sys

st.markdown("## Renumber PDB Atoms & Residues")
st.divider()

# File uploader
pdb_file = st.file_uploader(
    "Upload",
    type="pdb",
    help="**Input:** Protein PDB \n\n**Output:** PDB of renumbered atoms &/or residues"
)

# Optional
st.write("Optional")
start = st.number_input("Start", value=1, step=1, help="Number of the first residue in the renumbered file (default = 1)")
renumber_atoms = st.checkbox("Atoms", help="Renumbers atoms")
renumber_residues = st.checkbox("Residues", help="Renumbers residues")
chain_reset = st.checkbox("Chain Reset", help="Resets the residue renumbering after encountering a new chain")

# Check if a PDB file is uploaded
if pdb_file is not None:

    # Show the "Run" button
    if st.button("Run", help="Renumbering PDB Atoms & Residues"):
        with st.spinner("Running..."):
            time.sleep(2)

        with open("temp.pdb", "wb") as f:
            f.write(pdb_file.getvalue())

        # Construct the command to run the script with subprocess
        command = [
            "python",
            "renumber_pdb.py",
            "-i", "temp.pdb",
            "-s", str(start),
        ]

        if renumber_atoms:
            command.append("-a")
        if renumber_residues:
            command.append("-r")
        if chain_reset:
            command.append("-c")

        # Run the script using subprocess and capture the output
        result = subprocess.run(command, capture_output=True, text=True)

        # Display the output in Streamlit
        st.code(result.stdout)

        # Save PDB output to a temporary file
        temp_pdb2 = os.path.join("/tmp", "output.pdb")
        with open(temp_pdb2, "wb") as f:
            f.write(result.stdout.encode())

        # Download PDB via st.download
        st.markdown("## Download")
        with open(temp_pdb2, "rb") as f:
            renumbered_pdb_content = f.read()
        
        st.divider()

        st.download_button(label="Download Renumbered PDB", data=renumbered_pdb_content, file_name="output.pdb")

        # Remove the temporary PDB and FASTA files
        os.remove("temp.pdb")
        os.remove(temp_pdb2)
