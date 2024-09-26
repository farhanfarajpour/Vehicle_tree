import os

import psycopg2
import json
from datetime import datetime

from django.core.management.base import (
    BaseCommand, CommandError)

from vehicle_tree.settings import BASE_DIR


class Command(BaseCommand):
    help = 'add tree from excel file'

    def handle(self, *args, **kwargs):
        file_name = input("please enter the json name: ")
        print("starting to migrate the tree")
        conn = psycopg2.connect(database="mydb", user="negar", password="123", host="193.151.138.146", port=5432)
        cur = conn.cursor()

        def read_file(filename):
            fp = open(filename, 'r')
            data = fp.readlines()
            fp.close()
            return data

        out = read_file(os.path.join(BASE_DIR, "JSONS", file_name))

        json_data = [json.loads(item) for item in out]
        for item in json_data:
            for i in item:


                current_datetime = datetime.now()
                sql = """INSERT INTO vehicle_tree_app_menustree (
                                           id, created_at, parent_id, node_name_fa, updated_at, img_url, status, node_name_en, is_new,
                                           node_type_name, node_type_config_name, node_type_enum_id, node_type_config_id, fault_excel_info, node_type_feature_name,
                                            node_type_config_enum_id, Company_id, vehicle_id)
                                           VALUES (%s, %s, %s, %s, NULL, '', 'A', %s, False, %s, '' ,0, 0, '', '', 0,10001,1)"""

                values = (
                    int(i['ID']),
                    current_datetime,  # Use current datetime for created_at
                    int(i['ParentID']),
                    i['NodeNameFa'],
                    i['NodeNameEn'],
                    i['OldID'],
                )
                print(sql)
                cur.execute(sql, values)
                conn.commit()
