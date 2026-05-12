import os
import csv
import yaml
import subprocess


protein_csv = "ABL1_msa/abl_sequences.csv"
ligand_csv = "ligand_smile.csv"
output_dir = "./yaml_input"       
os.makedirs(output_dir, exist_ok=True)

def read_csv(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            data.append(row)
    return headers, data

protein_headers, proteins = read_csv(protein_csv)
print(f"The number of sequence: {len(proteins)}")

ligand_headers, ligands = read_csv(ligand_csv)
print(f"The number of ligands: {len(ligands)}")

required_protein_cols = ['id', 'sequence']
required_ligand_cols = ['name', 'smiles']


for protein in proteins:
    protein_id = protein['id']
    protein_seq = protein['sequence']
    a3m_file = f"ABL1_msa/{protein_id}.a3m"
    for ligand in ligands:
        ligand_name = ligand['name']
        ligand_smiles = ligand['smiles']
        
        yaml_data = {
            "version": 1,
            "sequences": [
                {
                    "protein": {
                        "id": "A",
                        "sequence": protein_seq,
                        "msa": a3m_file
                    }
                },
                {
                    "ligand": {
                        "id": "B",
                        "smiles": ligand_smiles
                    }
                }
            ],
            "properties": [
                {
                    "affinity": {
                        "binder": "B"
                    }
                }
            ]
        }
        
        safe_name = f"{protein_id}_{ligand_name}".replace("/", "_").replace("\\", "_")
        output_file = os.path.join(output_dir, f"{safe_name}.yaml")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_data, f, indent=2, default_flow_style=False, sort_keys=False)
        

        print("Running Boltz prediction...")
        cmd = ["boltz", "predict", str(output_file), "--out_dir",  "boltz_result_diff", "--no_kernels", "--diffusion_samples_affinity", str(32)]

        subprocess.run(cmd, check=True)
    print(f"Done {protein_id} !\n")

print("Completed")
