from pydantic import BaseModel
from typing import List
from datetime import datetime, date


class UserModel(BaseModel):
    id: int
    username: str
    agency_id: int
    agency_name: str


class EventModel(BaseModel):
    timestamp: str
    event_name: str
    properties: str | None


class UpdateUserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    mobile: str

class CreateUserSchema(BaseModel):
    username: str
    password: str

class ChangePasswordSchema(BaseModel):
    password: str
    confirm_password: str

class ElasticSaveSchema(BaseModel):
    id: int
    username: int
    first_name: str
    last_name: str
    # city: str