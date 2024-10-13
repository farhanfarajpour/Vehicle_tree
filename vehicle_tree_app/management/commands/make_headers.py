from vehicle_tree_app.models import MenusTree, Headers
import psycopg2
from django.core.management.base import (
    BaseCommand, CommandError)

class Command(BaseCommand):
    help = 'make headers table by enum_id'

    def handle(self, *args, **kwargs):
        # path = input("enter the path file to nodetypes:")
        with open('C:/Users/s.ghanbarzadeh/Desktop/isaco/diag_nodetype.h') as f:
            content = f.read()
        enums_list = []
        for enum in content.split(','):
            enum = enum.strip()
            if enum:
                enums_list.append(enum)

        menu = MenusTree.objects.all()
        for item in menu:
            if item.node_type_name in enums_list:
                print(item.node_name_en)
                headers = MenusTree.objects.filter(parent_id=item.id)
                for head in headers:
                    print(head.node_name_en)
                    Headers.objects.create(parent_id=item.node_type_enum_id,node_name_en=head.node_name_en,node_name_fa=head.node_name_fa,old_id=head.node_type_enum_id,menutree_id=item.id)
                    print("all done")