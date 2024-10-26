import os
import random
import string
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.crypto import get_random_string
from dns.tsig import validate
from prompt_toolkit.shortcuts import confirm
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, Token
from vehicle_tree_app.serializers.users.users_serializers import ChangePasswordSerializer
from vehicle_tree_app.repositories.base_repo import BaseRepo
from vehicle_tree_app.schemas.users import UpdateUserSchema, CreateUserSchema, ChangePasswordSchema
from vehicle_tree_app.services.sms.tasks import SendSms
from vehicle_tree_app.models.users import Users
from typing import List, Optional
from django.db.transaction import atomic
from django.conf import settings
import redis


class UsersRepo(BaseRepo):


    # ORM postgresql
    @atomic
    def get_users(self) -> List[Users]:
        return list(Users.objects.all())


    @atomic
    def login_user_by_phone(self, phone: str) -> Optional[Users]:
        user = Users.objects.filter(mobile=phone).first()
        if user:
            verification_code = get_random_string(length=4, allowed_chars='0123456789')
            SendSms.send_sms_task.delay(phone, verification_code)
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
    def update_user(self, user_id: int, data: UpdateUserSchema) -> Optional[Users]:
        user = self.get_user_by_id(user_id)
        if user:
            for attr, value in data.items():
                setattr(user, attr, value)
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
    def create_user(self, data: CreateUserSchema):
        username = data['username']
        if not Users.objects.filter(username=username).exists():
            new_user = Users(username=data["username"], password=data["password"])
            new_user.save()
            return new_user


    @atomic
    def change_password(self, data: ChangePasswordSchema):
        password = make_password(data['password'])
        user = Users(password=password)
        user.save()
        return user


    @atomic
    def get_redis(self, user):
        if user:
            return self.redis.get(f"user:{user.id}:logged_in")
        return False

    @atomic
    def set_redis(self, user_id: int, status: bool):
        if status:
            self.redis.set(f"user:{user_id}:logged_in", '1',3600)
        self.redis.delete(f"user:{user_id}:logged_in")

    @atomic
    def redis_active_users(self, user_id: int) -> bool:
        online_users_keys = self.redis.get('user:*:logged_in')
        online_users = []
        for key in online_users_keys:
            redis_user_id = key.decode().split(':')[1]
            online_users.append(redis_user_id)
        if str(user_id) in online_users:
            return True
        return False


    def redis_get_online_users(self):
        online_users_keys = self.redis.get('user:*:logged_in')
        online_users = [key.decode().split(':')[1] for key in online_users_keys]
        return online_users
