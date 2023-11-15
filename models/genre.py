from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from core import Base
from .base import Model


class Genre(Model, Base):

    __tablename__ = "genres"

    name = Column(String, nullable=False, index=True)
