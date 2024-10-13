from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

from vehicle_tree_app.models.menus import MenusTree
from vehicle_tree_app.models.base import BaseModel

class FaultMap(ExportModelOperationsMixin("FaultMap"),BaseModel):
    node_enum_name = models.ForeignKey(MenusTree, on_delete=models.CASCADE,related_name="node_enum_name")
    fault_detail_excel_name = models.CharField()
    v = models.CharField(max_length=255)
    p = models.JSONField(default=dict)
