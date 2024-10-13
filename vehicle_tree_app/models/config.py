from django.db import models
from django_prometheus.models import ExportModelOperationsMixin
from vehicle_tree_app.models import MenusTree
from vehicle_tree_app.models.base import BaseModel


class Configtype(ExportModelOperationsMixin("Configtype"), BaseModel):
    node_type_name = models.ForeignKey(MenusTree, on_delete=models.CASCADE, related_name="config_node_name")
    node_type_config_name = models.CharField(max_length=255, blank=True)
    node_type_config_id = models.IntegerField(default=0)
    # node_type_config_enum_id = models.IntegerField(default=0)
