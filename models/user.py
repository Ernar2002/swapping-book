from sqlalchemy import Column, String

from core import Base
from .base import Model


class User(Model, Base):

    __tablename__ = "users"

    email = Column(String(150), nullable=True, unique=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(150), nullable=True)
    last_name = Column(String(150), nullable=True)
    phone_number = Column(String(32))
