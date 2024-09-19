import psycopg2
import json
from datetime import datetime

# conn = psycopg2.connect(database="ngr_diag_db", user="postgres", password="Aaa0za560", host="localhost", port=5433)
conn = psycopg2.connect(database="postgres", user="postgres", password="Aaa0za560", host="192.168.4.252", port=5433)
cur = conn.cursor()


def read_file(filename):
    fp = open(filename, 'r')
    data = fp.readlines()
    fp.close()
    return data


def parent_to_table():

    out = read_file("minio_parent.json")

    json_data = [json.loads(item) for item in out]
    for json_str in json_data[0]:
        if json_str['OldID'] is None:
            json_str['OldID'] = ""
        current_datetime = datetime.now()
        sql = """INSERT INTO vehicle_tree_app_menustree (
                    id, created_at, parent_id, node_name_fa, updated_at, img_url, status, version, node_name_en, is_new, 
                    node_type_name, node_type_config_name, node_type_enum_id, node_type_config_id, fault_excel_info, node_type_feature_name,
                     node_type_config_enum_id, level, Company_id, vehicle_id) 
                    VALUES (%s, %s, %s, %s, NULL, '', 'A', 1, %s, False, %s, '' ,0, 0, '', '', 0, %s,1002,1001)"""

        values = (
            int(json_str['ID']),
            current_datetime,  # Use current datetime for created_at
            int(json_str['ParentID']),
            json_str['NodeNameFa'],
            json_str['NodeNameEn'],
            json_str['OldID'],
            json_str['Level']
        )
        print(sql)
        cur.execute(sql, values)
        conn.commit()


def child_to_table():

    out = read_file("minio_children.json")

    json_data = [json.loads(item) for item in out]
    for json_str in json_data[0]:
        current_datetime = datetime.now()
        sql = """INSERT INTO vehicle_tree_app_menustree (
                            id, created_at, parent_id, node_name_fa, updated_at, img_url, status, version, node_name_en, is_new, 
                            node_type_name, node_type_config_name, node_type_enum_id, node_type_config_id, fault_excel_info, node_type_feature_name,
                             node_type_config_enum_id, level, Company_id ,vehicle_id) 
                            VALUES (%s, %s, %s, %s, NULL, '', 'A', 1, %s, False, %s, '' ,0, 0, '', '', 0, %s,1002,1001)"""

        values = (
            int(json_str['ID']),
            current_datetime,  # Use current datetime for created_at
            int(json_str['ParentID']),
            json_str['NodeNameFa'],
            json_str['NodeNameEn'],
            json_str['OldID'],
            json_str['Level']
        )
        print(sql)
        cur.execute(sql, values)
        conn.commit()


parent_to_table()
child_to_table()


cur.close()
conn.close()
