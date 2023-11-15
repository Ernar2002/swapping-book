from sqlalchemy import Column, ForeignKey, Integer, String, TEXT, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from .base import Model


class Book(Model, Base):

    __tablename__ = "books"

    name = Column(String, nullable=False, index=True)
    publisher_id = Column(UUID(as_uuid=True),
                          ForeignKey("users.id"),
                          nullable=False)
    genre_id = Column(UUID(as_uuid=True),
                        ForeignKey("genres.id"),
                        nullable=True)
    author_id = Column(UUID(as_uuid=True),
                        ForeignKey("authors.id"),
                        nullable=True)
    year = Column(Integer)
    image_link = Column(TEXT, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    
    publisher = relationship("User", back_populates="books")
    genre = relationship("Genre", back_populates="books")
    author = relationship("Author", back_populates="books")
