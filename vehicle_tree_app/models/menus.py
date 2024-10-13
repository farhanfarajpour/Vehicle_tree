from django.db import models
from django_prometheus.models import ExportModelOperationsMixin
from vehicle_tree_app.models.base import BaseModel
from vehicle_tree_app.models.company import Company
from vehicle_tree_app.models.vehicle import Vehicle


class MenusTree(ExportModelOperationsMixin("menus"), BaseModel):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="vehicle", null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company", null=True, blank=True)
    parent_id = models.IntegerField()
    node_name_en = models.CharField(max_length=200, default='')
    node_name_fa = models.CharField(max_length=200)
    img_url = models.CharField(null=True, blank=True, max_length=250)

    # version = models.IntegerField(default=1)
    node_type_name = models.CharField(max_length=254, blank=True, null=True)
    # level = models.IntegerField(null=True, blank=True, default=None)
    # # A = Add, D = Delete, U = Update
    status = models.CharField(max_length=10, blank=True, default='A')

    # version = models.CharField(max_length=100, default='1.0')
    is_new = models.BooleanField(default=False)

    node_type_config_name = models.CharField(max_length=255, blank=True)
    node_type_enum_id = models.IntegerField(default=0)
    node_type_config_id = models.IntegerField(default=0)
    fault_excel_info = models.TextField(blank=True)
    node_type_feature_name = models.TextField(blank=True)
    node_type_config_enum_id = models.IntegerField(default=0)
    # reset_enum_id = models.IntegerField(null=True, blank=True)
    # reset_enum_name = models.CharField(blank=True)
