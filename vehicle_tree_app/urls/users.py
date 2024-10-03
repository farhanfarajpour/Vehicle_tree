from django.urls import path

from vehicle_tree_app.api.v1.users.users import (LoginByNumberForGetCodeView, LoginByUsernameView, LogoutView,
                                                 LoginByNumber, UserUpdateView,
                                                 UserDeleteView,
                                                 UserListView
                                                 )

user_url = [

    path('users/login', LoginByUsernameView.as_view(), name='LoginByUsername'),
    path('users/phone/verify', LoginByNumberForGetCodeView.as_view(), name='LoginByNumber'),
    path('users/login/phone', LoginByNumber.as_view(), name='Loginv'),
    path('users/logout', LogoutView.as_view(), name='Logout'),
    path('users/update', UserUpdateView.as_view(), name='Update'),
    path('users/delete', UserDeleteView.as_view(), name='Delete'),
    path('users/list', UserListView.as_view(), name='List'),
]
