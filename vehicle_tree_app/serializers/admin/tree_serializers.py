from rest_framework import serializers
from vehicle_tree_app.models import MenusTree


class AddMenusTreeSerializer(serializers.Serializer):
    parent_id = serializers.IntegerField(min_value=0, error_messages={
        'null': 'id cannot be null.',
        'invalid': 'Invalid id.'
    })
    node_name_en = serializers.CharField(min_length=1,max_length=100, error_messages={
        'null': 'node_name_en cannot be null.',
        'invalid': 'Invalid node_name_en.'
    })
    node_name_fa = serializers.CharField(min_length=1,max_length=100 , error_messages={
        'null': 'node_name_fa cannot be null.',
        'invalid': 'Invalid node_name_fa.'
    })

class UpdateMenusTreeSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
    node_name_en = serializers.CharField(required=False,min_length=1,max_length=100)
    node_name_fa = serializers.CharField(required=False,min_length=1,max_length=100)


class DeleteMenusTreeSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)

