from typing import Type
from pydantic import BaseModel
from vehicle_tree_app.schemas.users import UserModel


class UserIndexConfig:
    es_index_name = "users_index"
    es_index_mapping = {
        "properties": {
            "id": {"type": "integer"},
            "username": {"type": "text"},
            "first_name": {"type": "text"},
            "last_name": {"type": "text"},
            "city": {"type": "keyword"},
            "agency_id": {"type": "integer"},
            "agency_name": {"type": "text"}
        }
    }
    es_settings = {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }