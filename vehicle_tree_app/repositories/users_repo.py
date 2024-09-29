import random
import string

from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from vehicle_tree_app.repositories.base_repo import BaseRepo
from vehicle_tree_app.schemas.users import UpdateUserSchema
from vehicle_tree_app.services.sms.tasks import SendSms
from vehicle_tree_app.models.users import Users
from typing import List, Optional
from django.db.transaction import atomic


class UsersRepo(BaseRepo):

    # SMS Service
    @staticmethod
    def log_sms(phone_number: str, message: str):
        SendSms.send_sms_task.delay(phone_number, message)

    # ORM postgresql
    @atomic
    def get_users(self) -> List[Users]:
        return list(Users.objects.all())

    @atomic
    def login_user_by_phone(self, phone: str) -> Optional[Users]:
        user = Users.objects.filter(mobile=phone).first()
        if user:
            verification_code = get_random_string(length=4, allowed_chars='0123456789')
            message = f'کد تأیید شما: {verification_code}'
            SendSms.send_sms_task.delay(phone, message)
            user.code = verification_code
            user.save()
            return user
        return None

    @atomic
    def login_verify_user_code(self, phone: str, code: str) -> Optional[Users]:
        user = Users.objects.filter(mobile=phone, code=code).first()
        if user:
            return user
        return None

    @atomic
    def login_user_by_username(self, username: str, password: str) -> Optional[Users]:
        user_filter = Users.objects.filter(username=username)
        if user_filter:
            user = user_filter.first()
            if user.check_password(password):
                return user
        return None

    @atomic
    def get_user_by_id(self, user_id: int) -> Optional[Users]:
        return Users.objects.get(id=user_id)

    @atomic
    def check_new_user(self, phone_number: str) -> bool:
        return Users.objects.filter(phone=phone_number, is_new_user=False).exists()

    @atomic
    def update_user(self, user_id: int, data: UpdateUserSchema) -> Optional[Users]:
        # Retrieve the user by ID
        user = self.get_user_by_id(user_id)
        if user:
            # Update the user's fields with the new data
            for attr, value in data.items():
                setattr(user, attr, value)
            # Save the updated user instance
            user.save()
            return user
        return None
    @atomic
    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            user.delete()
            return True
        return False

    @atomic
    def get_total_user(self):
        return Users.objects.count()
