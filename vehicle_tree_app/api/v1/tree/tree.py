import os

from django.http import FileResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from vehicle_tree.settings import client
from vehicle_tree_app.injector.base_injector import BaseInjector
from vehicle_tree_app.models import MenusTree
from vehicle_tree_app.repositories.tree_repo import MenusTreeRepo
from vehicle_tree_app.repositories.company_repo import CompanyRepo
from rest_framework import generics, status
from sentry_sdk import capture_exception
from vehicle_tree_app.middleware.response import APIResponse
from vehicle_tree_app.repositories.vehicle_repo import VehicleRepo
from vehicle_tree_app.schemas.tree import MenuTreeModelSchema, UpdateMenuTreeModelSchema
from vehicle_tree_app.serializers.admin.tree_serializers import AddMenusTreeSerializer, UpdateMenusTreeSerializer, \
    DeleteMenusTreeSerializer
from vehicle_tree_app.utils.validations import ValidateAndHandleErrors
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView


class BaseView(APIView, AutoSchema):
    MenusTree_repo = BaseInjector.get(MenusTreeRepo)
    Vehicle_repo = BaseInjector.get(VehicleRepo)
    Company_Repo = BaseInjector.get(CompanyRepo)


class AllTree(BaseView, generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)

    # serializer_class = MenusTreeSerializer

    def get(self, request):
        try:
            tree = self.MenusTree_repo.get_all_tree()
            vehicle = self.Vehicle_repo.get_all_vehicle()
            company = self.Company_Repo.get_all_company()

            data = {
                'tree': [],
            }
            for c in vehicle:
                data['tree'].append({
                    'id': c.id,
                    'parent_id': c.parent_id,
                    'node_name_en': c.node_name_en,
                    'node_name_fa': c.node_name_fa,

                })
            for c in company:
                data['tree'].append({
                    'id': c.id,
                    'parent_id': c.parent_id,
                    'node_name_en': c.node_name_en,
                    'node_name_fa': c.node_name_fa,

                })

            for t in tree:
                data['tree'].append({
                    'id': t.id,
                    'parent_id': t.parent_id,
                    'node_name_en': t.node_name_en,
                    'node_name_fa': t.node_name_fa,

                })

            return Response(data)

        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)


class AddTree(BaseView, generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = AddMenusTreeSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            result = ValidateAndHandleErrors.validate_and_handle_errors(serializer)
            if result:
                return result

            if self.MenusTree_repo.create_item(MenuTreeModelSchema(**serializer.validated_data)):
                return APIResponse(success_code=2002, status=status.HTTP_201_CREATED)
            return APIResponse(error_code=5, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)


class UpdateTree(BaseView, generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateMenusTreeSerializer

    def put(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            result = ValidateAndHandleErrors.validate_and_handle_errors(serializer)
            if result:
                return result
            if self.MenusTree_repo.update_tree(UpdateMenuTreeModelSchema(**serializer.validated_data)):
                return APIResponse(success_code=2003, status=status.HTTP_201_CREATED)
            return APIResponse(error_code=4, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)


class DeleteTree(BaseView, generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = DeleteMenusTreeSerializer

    def delete(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            result = ValidateAndHandleErrors.validate_and_handle_errors(serializer)
            if result:
                return result
            if self.MenusTree_repo.delete_tree(id=serializer.validated_data.get("id")):
                return APIResponse(success_code=2004, status=status.HTTP_201_CREATED)
            else:
                return APIResponse(error_code=4, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)


class Img(BaseView, generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            file_name = f"{id}.png"
            bucket_name = os.environ.get("IMG_BUCKET")
            response = self.MenusTree_repo.service_minio.get_object(bucket_name, file_name)
            return FileResponse(response, as_attachment=True, filename=file_name)

        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id):
        try:
            file_name = f"{id}.png"
            bucket_name = os.environ.get("IMG_BUCKET")
            image = request.FILES.get("img")
            if self.MenusTree_repo.service_minio.update_object(bucket_name, file_name, image):
                return APIResponse(success_code=2005, status=status.HTTP_201_CREATED)
            return APIResponse(error_code=6, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return APIResponse(error_code=1, status=status.HTTP_400_BAD_REQUEST)
