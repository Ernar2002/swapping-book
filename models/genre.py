from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from core import Base
from .base import NamedModel


class Genre(NamedModel, Base):

    __tablename__ = "genres"
