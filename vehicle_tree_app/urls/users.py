from django.urls import path

from vehicle_tree_app.api.v1.users.users import (
    IndexView, Login
)


user_url = [


    path('Login', Login.as_view(), name='login'),

]