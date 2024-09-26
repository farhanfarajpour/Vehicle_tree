from pydantic import BaseModel
from typing import List
from datetime import datetime, date
from typing import Optional

class MenuTreeModelSchema(BaseModel):
    parent_id: int
    node_name_en: str
    node_name_fa: str


class UpdateMenuTreeModelSchema(BaseModel):
    id: int
    node_name_en: Optional[str] = None
    node_name_fa: Optional[str] = None

