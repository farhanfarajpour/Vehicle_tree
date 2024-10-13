from rest_framework import serializers
from vehicle_tree_app.models import MenusTree, Headers


class HeaderSerializer(serializers.ModelSerializer):
    menutree = serializers.CharField(source="menutree.node_type_name")
    class Meta:
        model = Headers
        fields = ("id", "parent_id", "node_name_en", "node_name_fa", "old_id", "menutree")
