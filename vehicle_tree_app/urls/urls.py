from django.urls import path, include
from vehicle_tree_app.urls.admin.admin import admin_url
from vehicle_tree_app.urls.users import user_url

urlpatterns = [

    # Admin
    path('', include(admin_url)),

    # User
    path('', include(user_url)),
]
