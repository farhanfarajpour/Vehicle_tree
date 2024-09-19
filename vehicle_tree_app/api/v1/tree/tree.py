from rest_framework.response import Response

from vehicle_tree_app.injector.base_injector import BaseInjector
from vehicle_tree_app.models import MenusTree
from vehicle_tree_app.repositories.tree_repo import MenusTreeRepo
from vehicle_tree_app.repositories.company_repo import CompanyRepo
from rest_framework import generics, status
from sentry_sdk import capture_exception
from vehicle_tree_app.middleware.response import APIResponse
from vehicle_tree_app.repositories.vehicle_repo import VehicleRepo
from vehicle_tree_app.serializers.admin.tree_serializers import MenusTreeSerializer
from vehicle_tree_app.utils.validations import ValidateAndHandleErrors
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView


class BaseView(APIView, AutoSchema):
    MenusTree_repo = BaseInjector.get(MenusTreeRepo)
    Vehicle_repo = BaseInjector.get(VehicleRepo)
    Company_Repo = BaseInjector.get(CompanyRepo)


class AllTree(BaseView, generics.GenericAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    # serializer_class = MenusTreeSerializer

    def get(self, request):
        try:
            tree = self.MenusTree_repo.get_all_tree()
            vehicle = self.Vehicle_repo.get_all_vehicle()
            company = self.Company_Repo.get_all_company()

            data = {
                'tree': [],
            }
            for c in vehicle :
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
