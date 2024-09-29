from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from sentry_sdk import capture_exception

import vehicle_tree_app
from vehicle_tree_app.injector.base_injector import BaseInjector
from vehicle_tree_app.models import users
from vehicle_tree_app.repositories.users_repo import UsersRepo
from vehicle_tree_app.serializers.users.users_serializers import (
    UserUpdateSerializer, UserLoginSerializer, UserNumberLoginSerializer, UserNumberCodeSerializer, UserDeleteSerializer
)
from vehicle_tree_app.models.users import Users
from rest_framework import permissions
from vehicle_tree_app.middleware.response import APIResponse
from vehicle_tree_app.services.sms.tasks import SendSms
from vehicle_tree_app.utils.validations import ValidateAndHandleErrors


class BaseView(APIView, AutoSchema):
    user_repo = BaseInjector.get(UsersRepo)


class IndexView(BaseView, generics.GenericAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    # serializer_class = UserInfoUpdateSerializer

    def get(self, request):
        """
        Update user information
        """
        try:
            self.user_repo.test_elk()
            sz = self.get_serializer(data=request.data)
            result = ValidateAndHandleErrors.validate_and_handle_errors(sz)
            if result:
                return result

            # TODO : ...

            return APIResponse(data=True)

        except Exception as e:
            capture_exception(e)
            return APIResponse(error_code=1, status=500)


class LoginByUsernameView(BaseView, generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):

        try:
            sz = self.get_serializer(data=request.data)
            result = ValidateAndHandleErrors.validate_and_handle_errors(sz)
            if result:
                return result
            user = self.user_repo.login_user_by_username(sz.data['username'], sz.data['password'])
            if user:
                token = AccessToken.for_user(user)
                refresh_token = RefreshToken.for_user(user)
                out = {
                    'token': f'{token}',
                    'refreshToken': f'{refresh_token}',

                }
                return APIResponse(data=out)
            else:
                return APIResponse(error_code=2, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)


class LoginByNumberForGetCodeView(BaseView, generics.GenericAPIView):
    serializer_class = UserNumberLoginSerializer

    def post(self, request):
        try:
            sz = self.get_serializer(data=request.data)
            result = ValidateAndHandleErrors.validate_and_handle_errors(sz)
            if result:
                return result
            user = self.user_repo.login_user_by_phone(sz.data['mobile'])
            if user:
                return APIResponse(success_code=2007)
            else:
                return APIResponse(error_code=4, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)


class LoginByNumber(BaseView, generics.GenericAPIView):
    serializer_class = UserNumberCodeSerializer

    def post(self, request):
        try:
            sz = self.get_serializer(data=request.data)
            result = ValidateAndHandleErrors.validate_and_handle_errors(sz)
            if result:
                return result
            user = self.user_repo.login_verify_user_code(sz.data['phone_number'], sz.data['code'])
            if user:
                token = AccessToken.for_user(user)
                refresh_token = RefreshToken.for_user(user)
                out = {
                    'token': f'{token}',
                    'refreshToken': f'{refresh_token}',
                }
                return APIResponse(data=out)
            else:
                return APIResponse(error_code=9, status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:

            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(BaseView, generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refreshToken")
            result = ValidateAndHandleErrors.validate_and_handle_errors(refresh_token)
            if result:
                return result
            if not refresh_token:
                return APIResponse(error_code=8, status=status.HTTP_400_BAD_REQUEST)
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                return APIResponse(error_code=7, status=status.HTTP_400_BAD_REQUEST)

            return APIResponse(2001, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:

            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(BaseView, generics.GenericAPIView):
    serializer_class = UserUpdateSerializer

    def put(self, request):
        try:
            sz = self.get_serializer(data=request.data)
            result = ValidateAndHandleErrors.validate_and_handle_errors(sz)
            if result:
                return result
            user = self.user_repo.update_user(user_id=request.data["id"], data=sz.validated_data)
            return APIResponse(success_code=2003, status=status.HTTP_200_OK)

        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(BaseView, generics.GenericAPIView):
    serializer_class = UserDeleteSerializer

    def delete(self, request):
        try:
            sz = self.get_serializer(data=request.data)
            result = ValidateAndHandleErrors.validate_and_handle_errors(sz)
            if result:
                return result
            user = self.user_repo.delete_user(user_id=request.data["id"])
            return APIResponse(success_code=2004, status=status.HTTP_200_OK)

        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)


class UserListView(BaseView, generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        try:
            sz = self.get_serializer(data=request.data)
            result = ValidateAndHandleErrors.validate_and_handle_errors(sz)
            if result:
                return result
            user = self.user_repo.get_users()
            serialized_users = UserLoginSerializer(users, many=True)
            return APIResponse(serialized_users.data, status=status.HTTP_200_OK)

        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)
