from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

from vehicle_tree_app.models import MenusTree
from vehicle_tree_app.models.base import BaseModel
from vehicle_tree_app.models.company import Company
from vehicle_tree_app.models.vehicle import Vehicle


class Headers(ExportModelOperationsMixin("headers"), BaseModel):
    menutree = models.ForeignKey(MenusTree, on_delete=models.CASCADE, default=None, null=True, blank=True)
    parent_id = models.IntegerField()
    node_name_en = models.CharField(max_length=200, default='')
    node_name_fa = models.CharField(max_length=200)
    old_id = models.CharField(max_length=200)

