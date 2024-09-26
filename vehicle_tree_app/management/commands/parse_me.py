import json
import os

import psycopg2
from django.core.management.base import (
    BaseCommand, CommandError)
import numpy as np
import pandas as pd
import string

from vehicle_tree.settings import BASE_DIR


class Command(BaseCommand):
    help = 'add tree from excel file'

    def handle(self, *args, **kwargs):
        file_path = input("please enter the file path: ")
        print("starting to parse the excel file")
        original_list = []
        for prefix in ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                       'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                       'U', 'V', 'W', 'X', 'Y', 'Z']:
            for letter in string.ascii_uppercase:
                original_list.append(prefix + letter)

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

        # file_path = 'D:/projects/Diag_Menu/02_Saipa.xlsm'
        # df = pd.read_excel(file_path,sheet_name="Sub_Unit")
        file_name = file_path.split('/')[-1]
        fp = open(os.path.join(BASE_DIR, "JSONS", f"{file_name}.json"), "w")
        excel_file = pd.ExcelFile(file_path)
        sheet_names = list(excel_file.sheet_names)
        data = []
        id = 10000
        first_id = id

        def Find_parent(parents: list):
            id = 0
            for parent in parents:
                for item in data:
                    if item['NodeNameEn'] == parent:
                        if parent == parents[0]:
                            id = item['ID']

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
                try:
                    df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=col)
                    df_cleaned = df.dropna(how='all')
                    if df_cleaned.empty:
                        break
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

                    break
        print("parsing the excel file is done")
        print(data)
        fp.write(json.dumps(data))
        fp.close()
        print("json file has been created")
