from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vehicle_tree.settings')
app = Celery('vehicle_tree')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'UTC'
app.autodiscover_tasks(['vehicle_tree_app'])
