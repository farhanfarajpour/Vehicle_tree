from django.urls import path, include
from vehicle_tree_app.urls.admin.admin import admin_url
from .users import user_url


urlpatterns = [

    path('', include(user_url)),
    # Admin
    path('', include(admin_url)),
]
