from rest_framework import serializers
from vehicle_tree_app.models import MenusTree


class MenusTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenusTree
        fields = ['id', 'parent_id', 'node_name_en', 'node_name_fa']
