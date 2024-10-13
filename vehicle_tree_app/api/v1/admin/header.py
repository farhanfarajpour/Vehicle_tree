import os

from django.http import FileResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from vehicle_tree.settings import client
from vehicle_tree_app.injector.base_injector import BaseInjector
from vehicle_tree_app.models import MenusTree
from vehicle_tree_app.repositories.header_repo import HeaderRepo
from vehicle_tree_app.repositories.tree_repo import MenusTreeRepo
from vehicle_tree_app.repositories.company_repo import CompanyRepo
from rest_framework import generics, status
from sentry_sdk import capture_exception
from vehicle_tree_app.middleware.response import APIResponse
from vehicle_tree_app.repositories.vehicle_repo import VehicleRepo
from vehicle_tree_app.schemas.tree import MenuTreeModelSchema, UpdateMenuTreeModelSchema
from vehicle_tree_app.serializers.admin.headers_serializers import HeaderSerializer
from vehicle_tree_app.serializers.admin.tree_serializers import AddMenusTreeSerializer, UpdateMenusTreeSerializer, \
    DeleteMenusTreeSerializer
from vehicle_tree_app.utils.validations import ValidateAndHandleErrors
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView


class BaseView(APIView, AutoSchema):
    Header_repo = BaseInjector.get(HeaderRepo)


class HeaderView(BaseView, generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):

        try:
            headers = self.Header_repo.filter_by_menutree_id(id)
            if headers:
                se = HeaderSerializer(headers, many=True)
                return Response(se.data, status=status.HTTP_200_OK)
        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)
