from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

from vehicle_tree_app.models.menus import MenusTree
from vehicle_tree_app.models.base import BaseModel

class ResetEnum(ExportModelOperationsMixin("ResetEnum"),BaseModel):
    node_enum_name = models.ForeignKey(MenusTree, on_delete=models.CASCADE,related_name="enum_name")
    reset_enum_name = models.CharField(blank=True)
    reset_enum_id = models.IntegerField(null=True, blank=True)
