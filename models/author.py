from sqlalchemy.orm import relationship

from core import Base
from .base import NamedModel


class Author(NamedModel, Base):

    __tablename__ = "authors"
    
    books = relationship("Book", back_populates="author",
                            cascade="all, delete")
