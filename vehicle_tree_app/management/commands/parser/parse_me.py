import json

import numpy as np
import pandas as pd
import string

original_list = []
for prefix in ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
               'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
               'U', 'V', 'W', 'X', 'Y', 'Z']:
    for letter in string.ascii_uppercase:
        original_list.append(prefix + letter)

# the output will be like: ['A', 'B', 'C','D','E','F','G','H','I', ..., 'Z', 'AA', 'AB', 'AC', ..., 'AZ', 'BA', 'BB', ..., 'ZZ']
vv = []
ls = []
for i in range(len(original_list)):
    if i % 6 == 0:
        nn = original_list[i:i + 5]
        if len(nn) == 5:
            gg = nn[0] + ":" + nn[4]
            ls.append(gg)
        if len(nn) == 3:
            gg = nn[0] + ":" + nn[2]
            ls.append(gg)

for i in range(len(original_list)):
    if i % 5 == 0:
        nn = original_list[i:i + 4]
        if len(nn) == 4:
            gg = nn[0] + ":" + nn[3]
            vv.append(gg)
        if len(nn) == 2:
            gg = nn[0] + ":" + nn[1]
            vv.append(gg)

file_path = 'D:/projects/Diag_Menu/01_IranKhodro.xlsm'
# df = pd.read_excel(file_path,sheet_name="Sub_Unit")
excel_file = pd.ExcelFile(file_path)
sheet_names = list(excel_file.sheet_names)
fp = open("./irankhodro.json", "w")
data = []

id = 1000
first_id = id


def Find_parent(parents: list):
    id = 0
    for parent in parents:
        for item in data:
            if item['NodeNameEn'] == parent:
                if parent == parents[0]:
                    id = item['ID']
                    parent_id = item['ParentID']

                else:
                    if item['ParentID'] == id:
                        id = item['ID']
                    else:
                        continue
    return id


for sheet_name in sheet_names:
    if sheet_name == 'Graph':
        break
    if sheet_name == 'Ecu_Menu':
        vv.clear()
        vv = ls
    for col in vv:
        final_json = []
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=col)
            df_cleaned = df.dropna(how='all')
            if df_cleaned.empty:
                break
            number_row = 1
            table = {"parent": [], "child": []}
            for i in range(0, len(df_cleaned)):
                if sheet_name == sheet_names[0]:
                    if str(df_cleaned.iloc[i, 0]) == 'nan':

                        data.append(
                            {
                                "ID": id + 1,
                                "ParentID": id,
                                "NodeNameEn": df_cleaned.iloc[i, 2],
                                "NodeNameFa": df_cleaned.iloc[i, 1],
                                "OldID": df_cleaned.iloc[i, 3] if str(df_cleaned.iloc[i, 3]) != 'nan' else "",
                            }
                        )

                    elif str(df_cleaned.iloc[i, 0]) != 'nan' and str(df_cleaned.iloc[i, 0]) != 'ردیف':
                        print(df_cleaned.iloc[i, 3])
                        data.append(
                            {
                                "ID": id + 1,
                                "ParentID": first_id + 1,
                                "NodeNameEn": df_cleaned.iloc[i, 2],
                                "NodeNameFa": df_cleaned.iloc[i, 1],
                                "OldID": df_cleaned.iloc[i, 3] if str(df_cleaned.iloc[i, 3]) != 'nan' else "",
                            }
                        )
                else:

                    if str(df_cleaned.iloc[i, 0]) == 'nan':
                        table['parent'].append(df_cleaned.iloc[i, 2])


                    elif str(df_cleaned.iloc[i, 0]) != 'nan' and str(df_cleaned.iloc[i, 0]) != 'ردیف':
                        parent_id = Find_parent(table['parent'])
                        data.append(
                            {
                                "ID": id + 1,
                                "ParentID": parent_id,
                                "NodeNameEn": df_cleaned.iloc[i, 2],
                                "NodeNameFa": df_cleaned.iloc[i, 1],
                                "OldID": df_cleaned.iloc[i, 3] if str(df_cleaned.iloc[i, 3]) != 'nan' else "",
                            }
                        )

                    elif str(df_cleaned.iloc[i, 0]) == 'ردیف':
                        table = {"parent": [], "child": []}
                        continue
                id = id + 1


        except Exception as e:
            print("no data")
            break
print(data)
fp.write(json.dumps(data))
fp.close()
