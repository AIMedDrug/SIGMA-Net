import pandas as pd

# 读取两个 CSV 文件
df1 = pd.read_csv('resistance_dG.csv')   # 列：ligand, mutation, resistance, dG
df2 = pd.read_csv('affinity_data_with_ddG.csv')   # 列：ligand, mutation, affinity_pred_value, ddG

df1.rename(columns={'dG': 'dG_exp'}, inplace=True)
df2.rename(columns={'ddG': 'ddG_pred'}, inplace=True)
# 按 ligand 和 mutation 进行外连接（保留所有匹配和不匹配的记录）
merged = pd.merge(df1, df2, on=['mutation', 'ligand'], how='outer')

# 保存合并后的结果
merged.to_csv('merged_boltz.csv', index=False)

print("合并完成，结果保存为 merged_boltz.csv")
