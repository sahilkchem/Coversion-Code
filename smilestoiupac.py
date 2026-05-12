#Imported Dependencies
import os
import sys
import time
import pandas as pd
import pubchempy as pcp

#Defined smiles2iupac function, use pandas for data manipulaton, use pcp for smiles api
def smiles_to_iupac(smiles):
    if pd.isna(smiles):
        return None
    smiles = str(smiles).strip()
    if not smiles:
        return None
    try:
        compounds = pcp.get_compounds(smiles, namespace="smiles")
        if compounds and compounds[0].iupac_name:
            return compounds[0].iupac_name
        return None
    except Exception as e:
        print(f"Skipping bad SMILES: {smiles}")
        print(f"Reason: {e}")
        return None
#Uses the directory the CSV file is in to export converted file
#If you want to place it in a different folder just input path directory in place of "base dir" 
def main():
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    input_file = os.path.join(base_dir, "molecules.csv")
    output_file = os.path.join(base_dir, "molecules_with_iupac.csv")

    print("BASE_DIR =", base_dir)
    print("INPUT_FILE =", input_file)
    print("OUTPUT_FILE =", output_file)

    df = pd.read_csv(input_file)
    df.columns = df.columns.str.strip().str.lower()

#Somestimes this code will not convert a name, may be a list issue
    if "smiles" not in df.columns:
        raise ValueError(f"No 'smiles' column found. Found columns: {df.columns.tolist()}")

    iupac_names = []

    for i, smi in enumerate(df["smiles"], start=1):
        iupac_names.append(smiles_to_iupac(smi))
        if i % 50 == 0:
            print(f"Processed {i} rows")
        time.sleep(0.1)

    df["iupac_name"] = iupac_names
    df.to_csv(output_file, index=False)
    print("Done. Saved to:", output_file)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR:", e)
    input("Press Enter to exit...")