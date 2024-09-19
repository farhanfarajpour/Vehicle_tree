from django.urls import path

from vehicle_tree_app.api.v1.tree.tree import AllTree

admin_url = [

    path('admin/all/menutree', AllTree.as_view(), name='list_of_all_menutree_diag'),


]
