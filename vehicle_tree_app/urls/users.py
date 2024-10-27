from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from vehicle_tree_app.api.v1.users.users import (LoginByNumberForGetCodeView, LoginByUsernameView, LogoutView,
                                                 LoginByNumber, UserUpdateView,
                                                 UserDeleteView,
                                                 UserListView,
ListActiveView,
ChangePasswordView,
CreateUserView)

user_url = [

    path('users/login', LoginByUsernameView.as_view(), name='LoginByUsername'),
    path('users/phone/verify', LoginByNumberForGetCodeView.as_view(), name='LoginFotGetCode'),
    path('users/login/phone', LoginByNumber.as_view(), name='LoginByNumber'),
    path('users/logout', LogoutView.as_view(), name='Logout'),
    path('users/update', UserUpdateView.as_view(), name='Update'),
    path('users/delete', UserDeleteView.as_view(), name='Delete'),
    path('users/list', UserListView.as_view(), name='List'),
    path('users/createuser', CreateUserView.as_view(), name='CreateUser'),
    path('users/changepassword', ChangePasswordView.as_view(), name='ChangePassword'),
    path('users/list/active', ListActiveView.as_view(), name='ListActive'),
    path('users/refresh',TokenRefreshView.as_view(), name='RefreshToken'),
]
