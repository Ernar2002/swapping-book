from typing import Optional

from .base import Model, ReadModel


class UserBase(Model):
    email: str
    first_name: str
    last_name: str
    phone_number: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class UserRead(UserBase, ReadModel):
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    
    class Config:
        orm_mode = True
