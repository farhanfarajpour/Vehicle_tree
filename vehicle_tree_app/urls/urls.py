from django.urls import path, include
from vehicle_tree_app.urls.admin.admin import admin_url


urlpatterns = [

    # Admin
    path('', include(admin_url)),

]
