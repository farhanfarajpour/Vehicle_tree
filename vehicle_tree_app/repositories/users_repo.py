import os
import random
import string
from http.client import responses
from operator import index

from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.crypto import get_random_string
from dns.tsig import validate
from elastic_transport import ObjectApiResponse
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from injector import inject
from prompt_toolkit.shortcuts import confirm
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, Token
from vehicle_tree_app.serializers.users.users_serializers import ChangePasswordSerializer
from vehicle_tree_app.repositories.base_repo import BaseRepo
from vehicle_tree_app.schemas.users import UpdateUserSchema, CreateUserSchema, ElasticSaveSchema, ChangePasswordSchema
from vehicle_tree_app.services.elastic_search import elastic_search
from vehicle_tree_app.services.redis.redis import RedisService
from vehicle_tree_app.services.sms.tasks import SendSms
from vehicle_tree_app.models.users import Users
from typing import List, Optional, Any, Dict
from django.db.transaction import atomic
from vehicle_tree_app.services.elastic_search.elastic_search import SearchELK
from django.conf import settings
import redis
from datetime import datetime


class UsersRepo(BaseRepo):
    @inject
    def __init__(self, elk: SearchELK, redis: RedisService):
        self.redis = redis
        self.elk = elk

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
            new_user = Users(username=data["username"], password=make_password(data["password"]))
            new_user.save()
            return new_user
        return None

    @atomic
    def change_password(self, data: ChangePasswordSchema):
        password = make_password(data['password'])
        user = Users(password=password)
        user.save()
        return user

    # REDIS
    @atomic
    def get_redis(self, user_id):
        return self.redis.get(f"user:{user_id}:logged_in")

    @atomic
    def set_redis(self, user_id: int, status: bool):
        if status is True:
            self.redis.set(f"user:{user_id}:logged_in", os.getenv('ONE'))
        elif status is False:
            self.redis.delete(f"user:{user_id}:logged_in")

    @atomic
    def redis_active_users(self, user_id: int) -> bool:
        online_users_keys = self.redis.keys('user:*:logged_in')
        if online_users_keys is None:
            online_users_keys = []
        online_users = []
        for key in online_users_keys:
            redis_user_id = key.decode().split(':')[os.getenv('ONE')]
            online_users.append(redis_user_id)
        if str(user_id) in online_users:
            return True
        return False

    @atomic
    def redis_get_online_users(self):
        online_users_keys = self.redis.keys('user:*:logged_in')
        if online_users_keys is None:
            online_users_keys = []
        online_users = [key.decode().split(':')[1] for key in online_users_keys]
        return online_users

    # ELASTIC_SEARCH
    @atomic
    def save_elasticsearch(self, data: ElasticSaveSchema) -> Optional[Users]:
        login_data = {
            'id': data.get('id'),
            'username': data.get('username'),
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
        }
        if not self.elk.check_index_exists():
            self.elk.create_index()
        self.elk.create_doc(login_data)
        user_id = data.get('id')
        user, created = Users.objects.get_or_create(
            id=user_id,
            defaults={
                'username': data.get('username'),
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
            }
        )
        if not created:
            user.username = data.get('username')
            user.first_name = data.get('first_name')
            user.last_name = data.get('last_name')
            user.save()
        return user
    @atomic
    def get_docs(self, index_name: str, query: dict = None):
        if query is None:
            query = {
                "query": {
                    "match_all": {}
                }
            }
        response = self.elk.get_doc(index_name=index_name, query=query)
        hits = response.get('hits', {}).get('hits', [])
        if hits:
            return response
        return {"error": "No documents found"}

    @atomic
    def search_docs(self, query: Dict[str, Any]):
        return self.elk.search(query=query)


    @atomic
    def save_elasticsearch_elk(self, data: ElasticSaveSchema) -> Optional[Users]:
        login_data = {
            'id': data.get('id'),
            'username': data.get('username'),
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
        }

        # Assuming `elk` is an instance of an Elasticsearch client
        if not self.elk.check_index_exists():
            self.elk.create_index()
        self.elk.create_doc(login_data)

        user_id = data.get('id')
        user, created = Users.objects.get_or_create(
            id=user_id,
            defaults={
                'username': data.get('username'),
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
            }
        )

        if not created:
            user.username = data.get('username')
            user.first_name = data.get('first_name')
            user.last_name = data.get('last_name')
            user.save()

        return user