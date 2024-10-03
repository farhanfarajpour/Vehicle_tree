import psycopg2
from django.core.management.base import (
    BaseCommand, CommandError)

class Command(BaseCommand):
    help = 'replace oldid to id'

    def handle(self, *args, **kwargs):
        path = input("enter the path file:")
        with open(path) as f:
            content = f.read()
        enums_list = []
        for enum in content.split(','):
            enum = enum.strip()
            if enum:
                enums_list.append(enum)

        conn = psycopg2.connect(database="mydb", user="negar", password="123", host="193.151.138.146", port=5432)
        cur = conn.cursor()
        cur.execute("""
                SELECT ALL node_type_name FROM vehicle_tree_app_menustree;
            """)

        new_data = cur.fetchall()
        for row in new_data:
            if row[0] in enums_list:
                id = enums_list.index(row[0])
                cur.execute("""
                            UPDATE vehicle_tree_app_menustree
                            SET node_type_enum_id = %s
                            WHERE node_type_name = %s;
                        """, (id, row[0]))
        conn.commit()
        print("done")

        # # Close the cursor and the connection
        cur.close()
        conn.close()
