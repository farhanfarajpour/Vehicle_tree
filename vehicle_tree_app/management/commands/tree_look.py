from anytree import Node, RenderTree
from django.core.management.base import (
    BaseCommand, CommandError)
import psycopg2

from collections import defaultdict

class Command(BaseCommand):
    help = 'see tree'

    def handle(self, *args, **kwargs):


        try:

            conn = psycopg2.connect(database="postgres", user="postgres", password="Aaa0za560", host="192.168.4.252", port=5433)
            cursor = conn.cursor()

            # Query to get all nodes
            cursor.execute("SELECT id, parent_id, node_name_en FROM vehicle_tree_app_menustree")
            rows = cursor.fetchall()

            # Create a dictionary to map parent_id to its children
            tree = defaultdict(list)
            for row in rows:
                node_id, parent_id, node_name = row
                tree[parent_id].append({"id": node_id, "name": node_name})


            # Step 4: Recursive function to build the anytree structure
            def build_anytree(node_id, name, parent=None):
                node = Node(name, parent=parent)  # Create a node
                for child in tree[node_id]:  # Loop through children of the current node
                    build_anytree(child["id"], child["name"], node)  # Recursively add children
                return node


            # Step 5: Find root nodes (parent_id is None)
            root_nodes = tree[0]

            # Step 6: Build and render the tree from the root nodes
            for root in root_nodes:
                root_node = build_anytree(root["id"], root["name"])

                # Render and print the tree structure
                for pre, fill, node in RenderTree(root_node):
                    print(f"{pre}{node.name}")

            # Step 7: Close database connection
            cursor.close()
            conn.close()

        except psycopg2.Error as e:
            raise CommandError(e)



