import json
from rdkit import Chem
import os

# Get the folder where this script is located(PLACE CSV IN SAME FOLDER AS SCRIPT)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FILE = os.path.join(BASE_DIR, "molecules.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "molecules.sdf")

#LOADING THE JSON FILE
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

writer = Chem.SDWriter(OUTPUT_FILE)

for i, entry in enumerate(data, start=1):
    smiles = entry.get("smiles")
    name = entry.get("name", "")

    if not smiles:
        print(f"Skipping entry {i}: no SMILES")
        continue

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        print(f"Invalid SMILES at entry {i}: {smiles}")
        continue

    #MOLECULE NAMER
    mol.SetProp("_Name", str(name))

    #ADD OTHER PROPERTIES
    for key, value in entry.items():
        if key != "smiles":
            try:
                mol.SetProp(str(key), str(value))
            except Exception:
                pass  # skip weird values

    writer.write(mol)

writer.close()

print(f"SDF file created at: {OUTPUT_FILE}")