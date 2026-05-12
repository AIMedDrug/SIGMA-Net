import os
import json
import glob
import csv

# ==================== 配置 ====================
base_dir = "boltz_result_diff"                     # 基础目录，可根据实际修改
output_csv = "affinity_results_diff.csv"           # 输出CSV文件名（可选，留空则不保存）

protein_csv = "ABL1_msa/abl_sequences.csv"
ligand_csv = "ligand_smile.csv"

# ==================== 读取CSV文件 ====================
def read_csv(file_path):
    """读取CSV文件，返回字段名列表和行字典列表"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            data.append(row)
    return headers, data

# 读取蛋白质数据
protein_headers, proteins = read_csv(protein_csv)
print(f"读取到 {len(proteins)} 条蛋白质记录")

# 读取配体数据
ligand_headers, ligands = read_csv(ligand_csv)
print(f"读取到 {len(ligands)} 条配体记录")

results = []   # 存储结果列表，每个元素为字典

for protein in proteins:
    protein_id = protein['id']
    for ligand in ligands:
        ligand_name = ligand['name']

        file_path = f"{base_dir}/boltz_results_{protein_id}_{ligand_name}/predictions/{protein_id}_{ligand_name}/affinity_{protein_id}_{ligand_name}.json"
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                affinity_value = data.get("affinity_pred_value")
                if affinity_value is None:
                    print(f"警告: {file_path} 中未找到 'affinity_pred_value' 键")
                    continue
                
                
                results.append({
                    "ligand": ligand_name,
                    "mutation":protein_id,
                    "affinity_pred_value": affinity_value
                })
            
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {file_path} - {e}")
            except Exception as e:
                print(f"读取文件出错: {file_path} - {e}")
        
if results:
    #print("\n=== 提取结果 ===")
    #for res in results:
    #    print(f"{res['ligand']}: {res['affinity_pred_value']}")
    
    # 可选：保存为CSV
    if output_csv:
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["ligand", "mutation", "affinity_pred_value"])
            writer.writeheader()
            writer.writerows(results)
        print(f"\n结果已保存至: {output_csv}")
        
else:
    print("未提取到任何有效数据。")
