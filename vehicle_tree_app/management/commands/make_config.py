import json
import os

from vehicle_tree_app.models import Configtype
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
        excel_file = pd.ExcelFile("C:/Users/s.ghanbarzadeh/Desktop/isaco/CONFIG_MAP.xlsx")
        sheet_names = list(excel_file.sheet_names)
        data = []

        def find_item(row, index, data):
            for item in data:
                if item["Excel Name"] == row:
                    item.update({"node_type_config_id": index})

        for sheet in sheet_names:
            if sheet == sheet_names[0]:
                df = pd.read_excel(excel_file, sheet_name=sheet_names[0])
                for index, row in df.iterrows():
                    item = {}
                    for col_idx, (col_name, value) in enumerate(row.items()):
                        if col_idx <= 1:
                            item.update({col_name: value})

                    data.append(item)
            elif sheet == sheet_names[1]:
                df = pd.read_excel(excel_file, sheet_name=sheet_names[1], header=None)
                for index, row in df.iterrows():
                    find_item(row[0], index, data)

        print(data)
        for item in data:
            enum_id = MenusTree.objects.filter(node_type_name=item["Node type"]).first()
            if enum_id:
                Configtype.objects.create(node_type_name_id=enum_id.id, node_type_config_name=item['Excel Name'],
                                          node_type_config_id=item['node_type_config_id'])
                print('done')
