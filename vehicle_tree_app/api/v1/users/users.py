from rest_framework import generics
from rest_framework.schemas import AutoSchema

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from vehicle_tree_app.injector.base_injector import BaseInjector
from vehicle_tree_app.middleware.exceptions import handle_exceptions
from vehicle_tree_app.middleware.validate import validate_serializer

from vehicle_tree_app.repositories.users_repo import UsersRepo
from vehicle_tree_app.serializers.users.users_serializers import (
    UserUpdateAndUserListSerializer, UserLoginSerializer, UserNumberLoginSerializer, UserNumberCodeSerializer,
    UserDeleteSerializer, CreateUserSerializer, ChangePasswordSerializer, UserLogoutSerializer, TokenSerializer
)
from vehicle_tree_app.permissions.permissions import IsAuthenticated, IsSuperUser
from vehicle_tree_app.models.users import Users
from rest_framework import permissions
from vehicle_tree_app.middleware.response import APIResponse
from vehicle_tree_app.services.sms.tasks import SendSms
from vehicle_tree_app.utils.validations import ValidateAndHandleErrors
from django.contrib.auth import authenticate, login
from django_redis import get_redis_connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import redis


class BaseView(APIView, AutoSchema):
    user_repo = BaseInjector.get(UsersRepo)


class LoginByUsernameView(BaseView, generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    @validate_serializer()
    @handle_exceptions
    def post(self, request):
        user = self.user_repo.login_user_by_username(request.data['username'], request.data['password'])
        if user:
            redis_conn = self.user_repo.get_redis_connection()
            logged_in = redis_conn.get(f"user:{user.id}:logged_in")
            redis_conn.set(f"user:{user.id}:logged_in", '1', ex=3600)
            out = TokenSerializer.get_tokens(user)
            if logged_in and logged_in.decode('utf-8') == '1':
                return APIResponse(error_code=12, status=status.HTTP_200_OK)
            return APIResponse(data=out)
        return APIResponse(error_code=2, status=status.HTTP_400_BAD_REQUEST)


class LoginByNumberForGetCodeView(BaseView, generics.GenericAPIView):
    serializer_class = UserNumberLoginSerializer

    @validate_serializer()
    @handle_exceptions
    def post(self, request):
        user = self.user_repo.login_user_by_phone(request.data['mobile'])
        if user:
            return APIResponse(success_code=2007)
        return APIResponse(error_code=4, status=status.HTTP_400_BAD_REQUEST)


class LoginByNumber(BaseView, generics.GenericAPIView):
    serializer_class = UserNumberCodeSerializer

    @validate_serializer()
    @handle_exceptions
    def post(self, request):
        user = self.user_repo.login_verify_user_code(request.data['phone_number'], request.data['code'])
        if user:
            redis_conn = self.user_repo.get_redis_connection()
            logged_in = redis_conn.get(f"user:{user.id}:logged_in")
            redis_conn.set(f"user:{user.id}:logged_in", '1', ex=3600)
            out =TokenSerializer.get_tokens(user)
            if logged_in and logged_in.decode('utf-8') == '1':
                return APIResponse(error_code=12, status=status.HTTP_200_OK, data=out)
            return APIResponse(data=out)
        return APIResponse(error_code=2, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(BaseView, generics.GenericAPIView):
    serializer_class = UserLogoutSerializer
    permission_classes = [IsAuthenticated]

    @validate_serializer()
    @handle_exceptions
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()
        redis_conn = self.user_repo.get_redis_connection()
        redis_conn.delete(f"user:{request.user.id}:logged_in")
        return APIResponse(success_code=2001, status=status.HTTP_205_RESET_CONTENT)


class UserUpdateView(BaseView, generics.GenericAPIView):
    serializer_class = UserUpdateAndUserListSerializer
    permission_classes = [IsSuperUser]

    @validate_serializer()
    @handle_exceptions
    def put(self, request):
        if self.user_repo.update_user(user_id=request.data["id"], data=request.data):
            return APIResponse(success_code=2003, status=status.HTTP_200_OK)
        return APIResponse(error_code=7, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(BaseView, generics.GenericAPIView):
    serializer_class = UserDeleteSerializer
    permission_classes = [IsSuperUser]

    @validate_serializer()
    @handle_exceptions
    def delete(self, request):
        if self.user_repo.delete_user(user_id=request.data["id"]):
            return APIResponse(success_code=2004, status=status.HTTP_200_OK)
        return APIResponse(error_code=4, status=status.HTTP_400_BAD_REQUEST)


class UserListView(BaseView, generics.GenericAPIView):
    serializer_class = UserUpdateAndUserListSerializer
    permission_classes = [IsSuperUser]

    def get(self, request):
        user = self.user_repo.get_users()
        if user:
            serialized_users = UserLoginSerializer(user, many=True)
            return APIResponse(serialized_users.data, status=status.HTTP_200_OK)
        return APIResponse(error_code=8, status=status.HTTP_400_BAD_REQUEST)


class CreateUserView(BaseView, generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [IsSuperUser]

    @validate_serializer()
    @handle_exceptions
    def post(self, request):
        user = self.user_repo.create_user(data=request.data)
        if user:
            return APIResponse(error_code=9, status=status.HTTP_400_BAD_REQUEST)
        return APIResponse(success_code=2008, status=status.HTTP_201_CREATED)


class ChangePasswordView(BaseView, generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsSuperUser]

    @validate_serializer()
    @handle_exceptions
    def post(self, request):
        self.user_repo.change_password(data=request.data)
        return APIResponse(success_code=2009, status=status.HTTP_201_CREATED)


class ListActiveView(BaseView, generics.GenericAPIView):
    permission_classes = [IsSuperUser]

    def get(self, request):
        online_user = self.user_repo.get_online_users()
        if online_user:
            return APIResponse({'online_users': online_user}, status=status.HTTP_200_OK)
        return APIResponse(error_code=13, status=status.HTTP_400_BAD_REQUEST)
