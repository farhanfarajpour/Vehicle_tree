from vehicle_tree_app.repositories.base_repo import BaseRepo
from vehicle_tree_app.schemas.tree import MenuTreeModelSchema, UpdateMenuTreeModelSchema
from vehicle_tree_app.schemas.users import UpdateUserSchema
from vehicle_tree_app.services.sms.tasks import SendSms
from vehicle_tree_app.models.headers import Headers
from typing import List, Optional
from django.db.transaction import atomic
from vehicle_tree_app.models.vehicle import Vehicle
from vehicle_tree_app.models.company import Company


class HeaderRepo(BaseRepo):

    # ORM postgresql
    @atomic
    def get_all_tree(self) -> Headers:
        return Headers.objects.all()

    @atomic
    def filter_by_menutree_id(self, id: int) -> Headers:
        return Headers.objects.filter(parent_id=id).all()
