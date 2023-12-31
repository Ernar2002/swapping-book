import uuid
import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Model(BaseModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class NamedModel(Model):
    name: str = Field(None)

    class Config:
        orm_mode = True

class ReadModel(Model):
    id: Optional[uuid.UUID]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True


class ReadNamedModel(NamedModel, ReadModel):
    name: Optional[str]

    class Config:
        orm_mode = True
