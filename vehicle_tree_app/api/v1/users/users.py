from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from sentry_sdk import capture_exception
from vehicle_tree_app.injector.base_injector import BaseInjector
from vehicle_tree_app.models import Users
from vehicle_tree_app.repositories.users_repo import UsersRepo
from vehicle_tree_app.serializers.users.users_serializers import (
    UserInfoUpdateSerializer, UsernameLoginSerializer
)
from rest_framework import permissions
from vehicle_tree_app.middleware.response import APIResponse
from vehicle_tree_app.services.sms.tasks import SendSms
from vehicle_tree_app.utils.validations import ValidateAndHandleErrors


class BaseView(APIView, AutoSchema):
    user_repo = BaseInjector.get(UsersRepo)


class Login(BaseView, APIView):
    serializer_class = UsernameLoginSerializer

    def post(self, request):

        try:
            se = UsernameLoginSerializer(data=request.data)
            result = ValidateAndHandleErrors.validate_and_handle_errors(se)
            if result:
                return result
            user = self.user_repo.login_user_by_username(se.validated_data['username'], se.validated_data['password'])
            if user:
                token = AccessToken.for_user(user)
                refresh_token = RefreshToken.for_user(user)
                out = {
                    'token': f'{token}',
                    'refresh_token': f'{refresh_token}',

                }
                return APIResponse(data=out)

            else:
                return APIResponse(error_code=2, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return APIResponse(success_code=2001, status=status.HTTP_200_OK)

        except Exception as e:
            return APIResponse(error_code=3, status=status.HTTP_400_BAD_REQUEST)
