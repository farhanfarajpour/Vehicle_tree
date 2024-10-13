import json
import os

from vehicle_tree_app.models import Configtype, ResetEnum
from vehicle_tree_app.models.menus import MenusTree

import psycopg2
from django.core.management.base import (
    BaseCommand, CommandError)
import numpy as np
import pandas as pd
import string


class Command(BaseCommand):
    help = 'make table config'

    def handle(self, *args, **kwargs):
        # path = input("enter the path file to nodetypes:")
        # fp = open(os.path.join(BASE_DIR, "JSONS", f"{file_name}.json"), "w")
        excel_file = pd.ExcelFile("C:/Users/s.ghanbarzadeh/Desktop/isaco/ResetEnum.xlsm")
        sheet_names = list(excel_file.sheet_names)
        data = []

        def find_item(row, index, data):
            for item in data:
                if item["reset_name"] == row:
                    item.update({"reset_id": index})

        for sheet in sheet_names:
            if sheet == sheet_names[0]:
                df = pd.read_excel(excel_file, sheet_name=sheet_names[0], header=None)
                for index, row in df.iterrows():
                    item = {}
                    for col_idx, (col_name, value) in enumerate(row.items()):
                        if col_idx == 0:
                            item.update({"enum_name": value})
                        elif col_idx == 1:
                            item.update({"reset_name": value})
                    data.append(item)
            elif sheet == sheet_names[1]:
                df = pd.read_excel(excel_file, sheet_name=sheet_names[1], header=None)
                for index, row in df.iterrows():
                    find_item(row[0], index, data)

        print(data)
        for item in data:
            enum_id = MenusTree.objects.filter(node_type_name=item["enum_name"]).first()
            if enum_id:
                ResetEnum.objects.create(node_enum_name_id=enum_id.id, reset_enum_name=item['reset_name'],
                                          reset_enum_id=item['reset_id'])
                print('done')
