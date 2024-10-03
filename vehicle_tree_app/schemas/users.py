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


class LogIndexModel(BaseModel):
    user: UserModel
    node_id: int
    operation_time: str
    operation_time_date: datetime
    node_route: str
    events_list: List[EventModel]
    created_at: datetime
