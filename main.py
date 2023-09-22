import os
import pandas as pd
from utils import print1
from utils import get_file_paths
from utils import getConfig
from compute import getData
from compute import compare

print1()
vcmID, ActuatorSN, VCMDataPath, buildDataPath, precision = getConfig()

total = 0
dfs = []  # 存储各个CSV文件的DataFrame
files = []  # 存储文件名

paths = get_file_paths(VCMDataPath)
for path in paths:
    df = getData(path)
    dfs.append(df)
    files.append(os.path.basename(path))

column_names = dfs[0].columns.tolist()  # 存储列名

# 使用concat()函数将多个DataFrame合并为一个DataFrame
vcmData = pd.concat(dfs, ignore_index=True)
# 过滤掉所有值都为NaN的行
vcmData = vcmData.dropna(how='all')
vcmData = vcmData[column_names]

# 读取Excel文件
df = getData(buildDataPath)
# 将列名 vcmID 改为 ActuatorSN
df.rename(columns={vcmID: ActuatorSN}, inplace=True)
df = df[column_names]
# 过滤掉所有值都为 "-" 的行
df = df[(df != "-").all(axis=1)]
# 重建索引
df = df.reset_index(drop=True)

total = compare(df, vcmData, ActuatorSN, precision)

print("total: ", total)
print("finished, please click Exit")
os.system("pause")  # 阻塞命令行窗口，直到用户按下任意键
