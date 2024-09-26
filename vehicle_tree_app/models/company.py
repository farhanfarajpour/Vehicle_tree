from django.db import models
from django_prometheus.models import ExportModelOperationsMixin
from vehicle_tree_app.models.base import BaseModel

class Company(ExportModelOperationsMixin("company"),BaseModel):
    node_name_en = models.CharField(max_length=200, default='')
    node_name_fa = models.CharField(max_length=200)
    parent_id = models.IntegerField()
