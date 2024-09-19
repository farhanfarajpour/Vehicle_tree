from vehicle_tree_app.repositories.base_repo import BaseRepo
from vehicle_tree_app.schemas.users import RegisterUserSchema
from vehicle_tree_app.services.sms.tasks import SendSms
from vehicle_tree_app.models.company import Company
from typing import List, Optional
from django.db.transaction import atomic
from vehicle_tree_app.models.vehicle import Vehicle
from vehicle_tree_app.models.company import Company


class CompanyRepo(BaseRepo):

    # ORM postgresql
    @atomic
    def get_all_company(self) -> Company:
        return Company.objects.all()
