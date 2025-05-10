import json
from elasticsearch import Elasticsearch, helpers
from click.core import batch
from django.core.paginator import Paginator
from dns.e164 import query
from elasticsearch.helpers import bulk
from django.contrib.sitemaps.views import index
from elastic_transport import ObjectApiResponse
from rest_framework import generics
from rest_framework.schemas import AutoSchema
from vehicle_tree_app.injector.base_injector import BaseInjector
from vehicle_tree_app.middleware.exceptions import handle_exceptions
from vehicle_tree_app.middleware.validate import validate_serializer
from vehicle_tree_app.repositories.users_repo import UsersRepo
from vehicle_tree_app.serializers.elasticsearch.elastic_serializers import LoginItemOfLogsSerializer, TokenSerializer, \
    SearchWithFirstnameSerializer, SearchWithLastnameSerializer, SearchWithCitySerializer, SearchWithUsernameSerializer
from vehicle_tree_app.permissions.permissions import IsAuthenticated, IsSuperUser
from rest_framework import permissions, status
from vehicle_tree_app.middleware.response import APIResponse
from rest_framework.views import APIView


class BaseView(APIView, AutoSchema):
    user_repo = BaseInjector.get(UsersRepo)


class LoginByUsernameView(BaseView, generics.GenericAPIView):
    serializer_class = LoginItemOfLogsSerializer

    @validate_serializer()
    @handle_exceptions
    def post(self, request):
        user = self.user_repo.save_elasticsearch(data=request.data)
        if user:
            out = TokenSerializer.get_tokens(user)
            return APIResponse(data=out)
        return APIResponse(error_code=9, status=status.HTTP_400_BAD_REQUEST)

class BulkInsertView(BaseView, generics.GenericAPIView):
    serializer_class = LoginItemOfLogsSerializer
    @validate_serializer()
    @handle_exceptions
    def post(self, request):
        users = request.data.get('users', [])
        for item in users:
            user = self.user_repo.save_elasticsearch_elk(data=item)
            if user:
                users.append(user)
        tokens = [TokenSerializer.get_tokens(user) for user in users]
        return APIResponse({"tokens": tokens}, status=status.HTTP_201_CREATED)


    # def post(self, request):
    #     users =request.data("users",[])
    #     for item in request.data:
    #         user = self.user_repo.save_elasticsearch(data=item)
    #         if user:
    #             users.append(user)
    #         else:
    #             return APIResponse(error_code=9, status=status.HTTP_400_BAD_REQUEST)
    #     tokens = [TokenSerializer.get_tokens(user) for user in users]
    #     return APIResponse(data=tokens)


class GetAllView(BaseView, generics.GenericAPIView):
    @handle_exceptions
    def get(self, request):
        query = {
            "query": {
                "match_all": {}
            }
        }
        page_number = request.GET.get('page', 1)
        page_size = 10
        start = (int(page_number) - 1) * page_size
        query.update({
            "from": start,
            "size": page_size
        })
        elk_data = self.user_repo.get_docs(index_name="users_index", query=query)
        hits = elk_data.get("hits", {}).get("hits", [])
        data = [
            {
                "id": hit["_source"].get("id"),
                "username": hit["_source"].get("username"),
                "first_name": hit["_source"].get("first_name"),
                "last_name": hit["_source"].get("last_name"),
                "city": hit["_source"].get("city"),
                "login_time": hit["_source"].get("login_time")
            }
            for hit in hits
        ]
        paginator = Paginator(data, page_size)
        page_obj = paginator.get_page(page_number)
        response_data = {
            "data": page_obj.object_list,
            "page_number": page_number,
            "total_pages": paginator.num_pages,
            "total_results": paginator.count
        }

        return APIResponse(data=response_data)


class SearchWithUsernameView(BaseView, generics.GenericAPIView):
    serializer_class = SearchWithUsernameSerializer

    @validate_serializer()
    @handle_exceptions
    def post(self, request, *args, **kwargs):
        query_body = {
            "query": {
                "bool": {
                    "must": []
                }
            }
        }
        username = request.data.get('username')
        if username:
            query_body["query"]["bool"]["must"].append({
                "match": {"username": username}
            })
        elk_data = self.user_repo.search_docs(query=query_body)
        if elk_data and isinstance(elk_data, dict):
            elk_data.get("hits", {}).get("hits", [])
        hits = elk_data.get("hits", {}).get("hits", [])
        data = [
            {
                "id": hit["_source"].get("id"),
                "username": hit["_source"].get("username"),
                "first_name": hit["_source"].get("first_name"),
                "last_name": hit["_source"].get("last_name"),
                "city": hit["_source"].get("city"),
                "login_time": hit["_source"].get("login_time")
            }
            for hit in hits
        ]

        return APIResponse(data)


class SearchWithFirstNameView(BaseView, generics.GenericAPIView):
    serializer_class = SearchWithFirstnameSerializer

    @validate_serializer()
    @handle_exceptions
    def post(self, request, *args, **kwargs):
        query_body = {
            "query": {
                "bool": {
                    "must": []
                }
            }
        }
        first_name = request.data.get('first_name')
        if first_name:
            query_body["query"]["bool"]["must"].append({
                "match": {"first_name": first_name}
            })
        elk_data = self.user_repo.search_docs(query=query_body)
        if elk_data and isinstance(elk_data, dict):
            elk_data.get("hits", {}).get("hits", [])
        hits = elk_data.get("hits", {}).get("hits", [])
        data = [
            {
                "id": hit["_source"].get("id"),
                "username": hit["_source"].get("username"),
                "first_name": hit["_source"].get("first_name"),
                "last_name": hit["_source"].get("last_name"),
                "city": hit["_source"].get("city"),
                "login_time": hit["_source"].get("login_time")
            }
            for hit in hits
        ]

        return APIResponse(data)


class SearchWithLastnameView(BaseView, generics.GenericAPIView):
    serializer_class = SearchWithLastnameSerializer

    @validate_serializer()
    @handle_exceptions
    def post(self, request, *args, **kwargs):
        query_body = {
            "query": {
                "bool": {
                    "must": []
                }
            }
        }
        last_name = request.data.get('last_name')
        if last_name:
            query_body["query"]["bool"]["must"].append({
                "match": {"last_name": last_name}
            })
        elk_data = self.user_repo.search_docs(query=query_body)
        if elk_data and isinstance(elk_data, dict):
            elk_data.get("hits", {}).get("hits", [])
        hits = elk_data.get("hits", {}).get("hits", [])
        data = [
            {
                "id": hit["_source"].get("id"),
                "username": hit["_source"].get("username"),
                "first_name": hit["_source"].get("first_name"),
                "last_name": hit["_source"].get("last_name"),
                "city": hit["_source"].get("city"),
                "login_time": hit["_source"].get("login_time")
            }
            for hit in hits
        ]

        return APIResponse(data)


class SearchWithCityView(BaseView, generics.GenericAPIView):
    serializer_class = SearchWithCitySerializer

    @validate_serializer()
    @handle_exceptions
    def post(self, request, *args, **kwargs):
        query_body = {
            "query": {
                "bool": {
                    "must": []
                }
            }
        }
        city = request.data.get('city')
        if city:
            query_body["query"]["bool"]["must"].append({
                "match": {"city": city}
            })
        elk_data = self.user_repo.search_docs(query=query_body)
        if elk_data and isinstance(elk_data, dict):
            elk_data.get("hits", {}).get("hits", [])
        hits = elk_data.get("hits", {}).get("hits", [])
        data = [
            {
                "id": hit["_source"].get("id"),
                "username": hit["_source"].get("username"),
                "first_name": hit["_source"].get("first_name"),
                "last_name": hit["_source"].get("last_name"),
                "city": hit["_source"].get("city"),
                "login_time": hit["_source"].get("login_time")
            }
            for hit in hits
        ]

        return APIResponse(data)


class BulkInsertView(BaseView, generics.GenericAPIView):

    @handle_exceptions
    def post(self, request):
        data = request.data.get('users', [])
        if not data:
            return APIResponse({"error": "No users data provided"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=data, many=True)
        if not serializer.is_valid():
            return APIResponse({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        success, failed = self.user_repo.save_elasticsearch_bulk(data)
        if success:
            out = TokenSerializer.get_tokens(data)
            return APIResponse(data=out, status=status.HTTP_201_CREATED)
        return APIResponse({"error_code": 9, "failed": failed}, status=status.HTTP_400_BAD_REQUEST)
