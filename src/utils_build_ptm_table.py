import os
import glob
import pandas as pd

# ---------------------------------------------------------
# PTM definitions
# ---------------------------------------------------------

ptm_dict = {
    'p': [79.9663],
    'me': [14.01565],
    'ox': [15.9949],
    'diox': [31.9898],
    'triox': [47.9847],
    'kin': [3.9949],
    'rev_ox': [-11.0337],
    'carb': [43.0053],
}

valid_residues = {
    'p': ['S','T','Y'],
    'me': ['M','E','H','T','C','K','N','Q','R','I','L','D','S'],
    'ox': ['M','Q','W','H','Y','C','D','K','N','P','R'],
    'diox': ['W','F','C','M','P','R','K','Y'],
    'triox': ['C','W','Y','F','M'],
    'rev_ox': ['C'],
    'carb': ['C'],
    'kin': ['W']
}

# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def assign_ptm(delta_mass, tol=0.01):
    """Assign a PTM based on delta mass and a tolerance threshold."""
    try:
        delta_mass = float(delta_mass)
    except:
        return None

    for ptm, masses in ptm_dict.items():
        for m in masses:
            if abs(delta_mass - m) < tol:
                return ptm
    return None


def load_file(filepath, sep):
    """Load a CSV or TSV file using the separator provided externally."""
    return pd.read_csv(filepath, sep=sep)


def process_dataframe(df):
    """
    Apply all preprocessing steps to a single DataFrame:
    - remove first line
    - select relevant columns
    - extract delta mass
    - assign PTMs
    - validate residues
    - generate binary PTM columns
    """

    # Remove first line
    df = df.iloc[1:].copy()

    # Select relevant columns
    df = df[['q','a','n','pgm']]

    # Extract delta mass
    df['delta_mass'] = pd.to_numeric(
        df['pgm'].str.split(';').str[1], errors='coerce'
    )
    df = df.drop(columns=['pgm'])
    df = df[df['delta_mass'].notna()].copy()

    # Assign PTMs
    df['ptm_type'] = df['delta_mass'].apply(assign_ptm)

    # Remove duplicates
    df = df.drop_duplicates(subset=['q','a','n','ptm_type','delta_mass'])

    # Create binary PTM columns
    ptm_types = df['ptm_type'].dropna().unique()
    for ptm in ptm_types:
        df[ptm] = (df['ptm_type'] == ptm).astype(int)

    # Final structure
    df_final = df[['q','a','n'] + list(ptm_types)].copy()
    df_final = df_final.rename(columns={'q':'protein_id','a':'AA','n':'position'})

    # Remove rows with no PTMs
    df_final = df_final[df_final[list(ptm_types)].sum(axis=1) > 0]

    # Validate residues
    for ptm, residues in valid_residues.items():
        if ptm in df_final.columns:
            df_final.loc[
                ~df_final['AA'].isin(residues) & (df_final[ptm] == 1),
                ptm
            ] = 0

    return df_final


def process_all_files(input_folder, output_folder, sep):
    """
    Process all files in the input folder and export cleaned files
    to the output folder with modified names.
    """

    os.makedirs(output_folder, exist_ok=True)

    # Detect extension based on separator
    extension = ".tsv" if sep == "\t" else ".csv"
    input_files = glob.glob(os.path.join(input_folder, f"*{extension}"))

    print(f"Found {len(input_files)} files to process.")

    for input_file in input_files:
        print(f"\nProcessing {input_file}")

        df = load_file(input_file, sep=sep)
        df_final = process_dataframe(df)

        # Build new filename
        base = os.path.basename(input_file)
        name, ext = os.path.splitext(base)
        new_name = f"{name}_ptm{ext}"

        output_file = os.path.join(output_folder, new_name)
        df_final.to_csv(output_file, index=False, sep=sep)

        print(f"Saved {output_file}")
