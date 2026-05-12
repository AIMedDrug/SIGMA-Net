import pandas as pd
import numpy as np

# ==================== 配置 ====================
input_file = "affinity_results_diff.csv"   # 输入文件名，请根据实际情况修改
output_file = "affinity_data_with_ddG.csv"  # 输出文件名（可选，也可覆盖原文件）

# ==================== 读取数据 ====================
df = pd.read_csv(input_file)

# 检查必要的列是否存在
required_cols = ['ligand', 'mutation', 'affinity_pred_value']

print(f"原始数据行数: {len(df)}")
print("数据示例:")
print(df.head())

# ==================== 提取WILD基准值 ====================
# 筛选出 mutation 为 'WILD' 的行
wild_df = df[df['mutation'] == 'WILD']
# 创建 ligand -> wild_affinity 的字典
wild_dict = dict(zip(wild_df['ligand'], wild_df['affinity_pred_value']))

print(f"\n找到 {len(wild_dict)} 个配体的WILD基准值:")
for lig, val in wild_dict.items():
    print(f"  {lig}: {val}")

# ==================== 计算ddG ====================
# 初始化新列，默认为NaN
df['ddG'] = np.nan

# 只对非WILD行进行计算
mask = df['mutation'] != 'WILD'
df.loc[mask, 'ddG'] = df.loc[mask].apply(
    lambda row: row['affinity_pred_value'] - wild_dict.get(row['ligand'], np.nan),
    axis=1
)

# 可选：如果某个ligand没有WILD基准，打印警告
missing_wild = df.loc[mask & df['ddG'].isna(), 'ligand'].unique()
if len(missing_wild) > 0:
    print(f"\n警告: 以下配体没有对应的WILD基准值，ddG设为NaN: {list(missing_wild)}")

# ==================== 保存结果 ====================
df.to_csv(output_file, index=False)
print(f"\n处理完成！结果已保存至: {output_file}")
print("\n结果数据示例（前10行）:")
print(df.head(10))

# 可选：显示统计信息
print("\nddG统计信息:")
print(df['ddG'].describe())
