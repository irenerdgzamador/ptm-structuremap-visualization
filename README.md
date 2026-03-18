# PTM PREPROCESSING & STRUCTUREMAP PIPELINE

This project processes raw peptide modification files, builds a binary PTM table, integrates it with AlphaFold structural models using StructureMap, and generates 1D/3D visualizations for downstream analysis.

The pipeline is modular and organized in three main notebooks:

- 01_build_ptm_table.ipynb → PTM preprocessing  
- 02_run_structuremap.ipynb → structural annotation and analysis  
- 03_plots.ipynb → visualizations (1D and 3D)

---

## 1. PROJECT STRUCTURE

```
project_ptms/
    config.yaml
    run_preprocessing.py
    requirements.txt
    env_py38/
    src/
        utils_build_ptm_table.py
    data/
        proteins.txt
        raw/
        processed/
    notebooks/
        01_build_ptm_table.ipynb
        02_run_structuremap.ipynb
        03_plots.ipynb
    README.md
```




---

## 2. REQUIREMENTS

### 2.1 Python environment

- Python 3.8 (recommended for StructureMap)
- All required packages are listed in requirements.txt

Create and activate a virtual environment (Windows):

cd C:\path\to\project_ptms
py -3.8 -m venv env_py38
env_py38\Scripts\activate.bat
pip install -r requirements.txt


In VS Code:

1. View > Command Palette > Python: Select Interpreter  
2. Choose env_py38\Scripts\python.exe  
3. Confirm the environment name appears in the bottom bar  

---

## 3. CONFIGURATION

The main configuration for PTM preprocessing is in config.yaml:

	input_folder: "data/raw"

	output_folder: "data/processed"

	separator: "," or separator: "\t"


You must also provide:

	data/proteins.txt  → one UniProt ID per line



---

## 4. PIPELINE OVERVIEW

### 4.1 Notebook 01 – PTM preprocessing

- Loads raw peptide/PTM files  
- Cleans and filters data  
- Assigns PTMs based on delta mass and residue  
- Generates a binary PTM table  
- Saves the final table in data/processed/ptm_table/ptm_table.tsv  

---

### 4.2 Notebook 02 – StructureMap core analysis

- Reads proteins.txt  
- Downloads AlphaFold CIF and PAE files  
- Computes pPSE and accessibility  
- Identifies IDRs  
- Merges AlphaFold annotation with the PTM table  
- Performs:
  - PTM colocalization  
  - Enrichment analysis in IDRs  

**Important:**  
Plots generated in this notebook (colocalization and enrichment) are not saved automatically.  
They must be saved manually from the Plotly interface or viewed directly in the notebook.

---

### 4.3 Notebook 03 – StructureMap visualizations

Generates:

- 1D plots:
  - pPSE along the sequence  
  - pPSE + PTMs  
  - IDR profiles  
  - Domains and regions + PTMs  

- 3D visualizations (py3Dmol):
  - pPSE  
  - pLDDT  
  - PTM sites  
  - Domains + PTMs  

All outputs are saved in:

S:\U_Proteomica\LABS\LAB_BI\Proyecto_IR_PTMs\StructureMap_output\plots


---

## 5. HOW TO RUN THE PIPELINE

### 5.1 Step 1 – Build the PTM table

Option A – Terminal:

cd project_ptms
env_py38\Scripts\activate.bat
python run_preprocessing.py



Option B – Notebook:

Open notebooks/01_build_ptm_table.ipynb

---

### 5.2 Step 2 – Run StructureMap core analysis

Open notebooks/02_run_structuremap.ipynb

This notebook:

- Downloads AlphaFold models  
- Computes pPSE and IDRs  
- Merges structural and PTM data  
- Runs colocalization and enrichment analyses  

---

### 5.3 Step 3 – Generate plots and 3D visualizations

Open notebooks/03_plots.ipynb

This notebook:

- Loads tables from Notebook 02  
- Creates 1D and 3D visualizations  
- Saves all outputs in the SC drive  

---

## 6. WHAT THE PIPELINE DOES (SUMMARY)

### Preprocessing (Notebook 01)

- Loads raw CSV/TSV files  
- Cleans and filters data  
- Extracts delta masses  
- Assigns PTMs  
- Validates residues  
- Creates binary PTM columns  
- Saves ptm_table.tsv  

### Structural analysis (Notebook 02)

- Downloads AlphaFold models  
- Computes pPSE  
- Identifies IDRs  
- Integrates PTMs  
- Evaluates PTM colocalization  
- Tests enrichment in IDRs  

### Visualization (Notebook 03)

- Generates 1D plots  
- Generates 3D interactive visualizations  
- Exports HTML, PNG, and PDF files  

---

## 7. NOTES

The code is modular and reproducible:

- Scripts for automation  
- Notebooks for exploration and documentation  

## Acknowledgements

This project incorporates components and workflows inspired by the StructureMap pipeline developed by the original authors. StructureMap is publicly available and distributed under an open-source license. The original repository and documentation can be found at:

https://github.com/MannLabs/structuremap

Some functions and analytical steps used in this project are adaptations or extensions of the original StructureMap implementation. All credit for the development of StructureMap and its underlying methodology belongs to its authors.
