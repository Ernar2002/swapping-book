from .base import NamedModel, ReadNamedModel


class GenreBase(NamedModel):
    pass


class GenreCreate(GenreBase):
    pass


class GenreUpdate(GenreBase):
    pass


class GenreRead(GenreBase, ReadNamedModel):
    pass

    class Config:
        orm_mode = True