from django.contrib.auth.password_validation import validate_password
from dns.dnssec import validate
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from sentry_sdk import capture_exception
import vehicle_tree_app
from vehicle_tree_app.injector.base_injector import BaseInjector
from vehicle_tree_app.middleware.validate import validate_serializer
from vehicle_tree_app.models import users
from vehicle_tree_app.repositories.users_repo import UsersRepo
from vehicle_tree_app.schemas.users import CreateUserSchema
from vehicle_tree_app.serializers.users.users_serializers import (
    UserUpdateAndUserListSerializer, UserLoginSerializer, UserNumberLoginSerializer, UserNumberCodeSerializer,
    UserDeleteSerializer, CreateUserSerializer, ChangePasswordSerializer, UserLogoutSerializer
)
from vehicle_tree_app.permissions.permissions import IsAuthenticated, IsSuperUser
from vehicle_tree_app.models.users import Users
from rest_framework import permissions
from vehicle_tree_app.middleware.response import APIResponse
from vehicle_tree_app.services.sms.tasks import SendSms
from vehicle_tree_app.utils.validations import ValidateAndHandleErrors


class BaseView(APIView, AutoSchema):
    user_repo = BaseInjector.get(UsersRepo)


class LoginByUsernameView(BaseView, generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    @validate_serializer()
    def post(self, request):

        try:
            user = self.user_repo.login_user_by_username(request.data['username'], request.data['password'])
            if user:
                token = AccessToken.for_user(user)
                refresh_token = RefreshToken.for_user(user)
                out = {
                    'token': f'{token}',
                    'refreshToken': f'{refresh_token}',

                }
                return APIResponse(data=out)
            return APIResponse(error_code=2, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)


class LoginByNumberForGetCodeView(BaseView, generics.GenericAPIView):
    serializer_class = UserNumberLoginSerializer

    @validate_serializer()
    def post(self, request):
        try:
            user = self.user_repo.login_user_by_phone(request.data['mobile'])
            if user:
                return APIResponse(success_code=2007)
            return APIResponse(error_code=4, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)


class LoginByNumber(BaseView, generics.GenericAPIView):
    serializer_class = UserNumberCodeSerializer

    @validate_serializer()
    def post(self, request):
        try:
            user = self.user_repo.login_verify_user_code(request.data['phone_number'], request.data['code'])
            if user:
                token = AccessToken.for_user(user)
                refresh_token = RefreshToken.for_user(user)
                out = {
                    'token': f'{token}',
                    'refreshToken': f'{refresh_token}',
                }
                return APIResponse(data=out)
            return APIResponse(error_code=9, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(BaseView, generics.GenericAPIView):
    serializer_class = UserLogoutSerializer
    permission_classes = [IsAuthenticated]

    @validate_serializer()
    def post(self, request):
        try:
            if not request.refresh_token:
                return APIResponse(error_code=3, status=status.HTTP_400_BAD_REQUEST)
            try:
                token = RefreshToken(request.refresh_token)
                token.blacklist()
            except Exception as e:
                return APIResponse(error_code=11, status=status.HTTP_400_BAD_REQUEST)
            return APIResponse(2001, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(BaseView, generics.GenericAPIView):
    serializer_class = UserUpdateAndUserListSerializer
    permission_classes = [IsSuperUser]

    @validate_serializer()
    def put(self, request):
        try:
            if self.user_repo.update_user(user_id=request.data["id"], data=request.data):
                return APIResponse(success_code=2003, status=status.HTTP_200_OK)
            return APIResponse(error_code=7, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(BaseView, generics.GenericAPIView):
    serializer_class = UserDeleteSerializer
    permission_classes = [IsSuperUser]

    @validate_serializer()
    def delete(self, request):
        try:
            if self.user_repo.delete_user(user_id=request.data["id"]):
                return APIResponse(success_code=2004, status=status.HTTP_200_OK)
            return APIResponse(error_code=4, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)


class UserListView(BaseView, generics.GenericAPIView):
    serializer_class = UserUpdateAndUserListSerializer
    permission_classes = [IsSuperUser]

    def get(self, request):
        try:
            user = self.user_repo.get_users()
            if user:
                serialized_users = UserLoginSerializer(user, many=True)
                return APIResponse(serialized_users.data, status=status.HTTP_200_OK)
            return APIResponse(error_code=8, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)


class CreateUserView(BaseView, generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [IsSuperUser]

    @validate_serializer()
    def post(self, request):
        try:
            user = self.user_repo.create_user(data=request.data)
            if user:
                return APIResponse(error_code=9, status=status.HTTP_400_BAD_REQUEST)
            return APIResponse(success_code=2008, status=status.HTTP_201_CREATED)
        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(BaseView, generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsSuperUser]

    @validate_serializer()
    def post(self, request):
        try:
            self.user_repo.change_password(data=request.data)
            return APIResponse(success_code=2009, status=status.HTTP_201_CREATED)
        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)
