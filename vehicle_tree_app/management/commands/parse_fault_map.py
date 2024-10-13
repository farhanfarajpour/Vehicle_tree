import json
import os
from vehicle_tree_app.models.fault_mapping import FaultMap
from vehicle_tree_app.models.menus import MenusTree


import psycopg2
from django.core.management.base import (
    BaseCommand, CommandError)
import numpy as np
import pandas as pd
import string
class Command(BaseCommand):
    help = 'make table Fault_Mapping'

    def handle(self, *args, **kwargs):
        # path = input("enter the path file to nodetypes:")
        # fp = open(os.path.join(BASE_DIR, "JSONS", f"{file_name}.json"), "w")
        excel_file = pd.ExcelFile("C:/Users/s.ghanbarzadeh/Desktop/isaco/Fault_Mapping.xlsx")
        sheet_names = list(excel_file.sheet_names)
        data = []

        df = pd.read_excel(excel_file, sheet_name=sheet_names[0])
        df_cleaned = df.dropna(how='all')
        for index, row in df.iterrows():

            item = {}
            # Iterate over columns in the current row
            for col_idx, (col_name, value) in enumerate(row.items()):
                if col_idx == 0:
                    item.update({"enum_name": value})
                elif col_idx == 1:
                    item.update({"FAUL DETAIL EXCEL NAME": value if str(value) != "nan" else 0})
                elif col_idx == 2:
                    item.update({"V": value if str(value) != "nan" else 0})
                elif col_idx >= 3:
                    if type(value) == str:
                        parent = value
                        child = []
                    if type(value) == int or type(value) == float:
                        if str(value) == 'nan':
                            continue
                        child.append(int(value))
                        item.update({parent: child})

            data.append(item)
        print(data)
        for item in data:
            enum_id = MenusTree.objects.filter(node_type_name=item["enum_name"]).first()
            if enum_id:
                keys_to_remove = ['enum_name', 'FAUL DETAIL EXCEL NAME', 'V']
                p = item.copy()
                for key in keys_to_remove:
                    del p[key]
                FaultMap.objects.create(node_enum_name_id=enum_id.id,fault_detail_excel_name=item['FAUL DETAIL EXCEL NAME'],v=item["V"],p=p)
                print('done')