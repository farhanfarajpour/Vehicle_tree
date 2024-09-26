from django.urls import path

from vehicle_tree_app.api.v1.tree.tree import AllTree, AddTree, UpdateTree, DeleteTree, Img

admin_url = [

    path('admin/all/menutree', AllTree.as_view(), name='list_of_all_menutree_diag'),
    path('admin/add/menutree', AddTree.as_view(), name='add_new_item_to_tree'),
    path('admin/update/menutree', UpdateTree.as_view(), name='update_item_tree'),
    path('admin/delete/menutree', DeleteTree.as_view(), name='delete_item_tree'),
    path('admin/download/<int:id>', Img.as_view(), name='SearchAndDownload'),
    path('admin/addimg/<int:id>', Img.as_view(), name='get_img'),

]
