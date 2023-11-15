import uuid

from typing import Optional

from .base import NamedModel, ReadNamedModel


class BookBase(NamedModel):
    genre_id: uuid.UUID
    author_id: uuid.UUID
    year: int
    image_link: Optional[str]


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookRead(BookBase, ReadNamedModel):
    publisher_id: Optional[uuid.UUID]
    genre_id: Optional[uuid.UUID]
    author_id: Optional[uuid.UUID]
    year: Optional[int]
    is_active: Optional[bool]

    class Config:
        orm_mode = True