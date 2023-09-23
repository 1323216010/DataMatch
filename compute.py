import re
import pandas as pd
import numpy as np
from utils import check_path_type
def getData(path):
    df = pd.DataFrame()

    if(check_path_type(path) == 'csv'):
        df = pd.read_csv(path, header=0)
    elif(check_path_type(path) == 'xlx' or check_path_type(path) == 'xlsx'):
        df = pd.read_excel(path)

    # 过滤掉列名中包含'Unnamed'的列
    filtered_columns = [col for col in df.columns if not re.match(r'^Unnamed', col)]
    # 选择需要的列
    df = df[filtered_columns]

    return df

#根据id去匹配，比较两个DataFrame的数值
def compare(df1, df2, id, precision):
    total = 0
    list1 = []
    list2 = []

    # 遍历DataFrame1的每一行
    for index, row in df1.iterrows():
        actuator_sn = row[id]  # 获取当前行的ActuatorSN

        # 在DataFrame2中查找匹配的行
        matching_rows = df2[df2[id] == actuator_sn]

        # 检查DataFrame1当前行的所有数据是否与DataFrame2匹配
        if len(matching_rows) == 0:
            list1.append(actuator_sn)
            print(actuator_sn, "can not be found in vcm data")
        else:
            row2 = matching_rows.iloc[0]

            # 检查DataFrame1当前行和DataFrame2匹配行的每一个元素是否相等
            # 使用 iteritems() 方法遍历索引和值
            for index, value in row.items():
                # if not np.isclose(row.at[index], row2.at[index]):
                if index != id and ~np.isclose(value, row2.at[index], atol=float(precision)):
                    total += 1
                    list2.append(actuator_sn)
                    print(index, " of ", actuator_sn, " is not match:")
                    print("build value:", value, " | ", "vcm data:", row2.at[index])
                    break
    if len(list1) !=0 or len(list2) != 0:
        tb = pd.DataFrame()
        if len(list1) !=0:
            tb['not_find'] = list1
        if len(list2) != 0:
            tb['not_match'] = list2
        # 将 DataFrame 存储为 Excel 文件
        tb.to_excel('MatchResult.xlsx', index=False, sheet_name='MatchResults')
        print("The MatchResult.xlsx file has been generated.")
    return total