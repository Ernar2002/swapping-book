from sqlalchemy.orm import Session

from models import Genre
from schemas import GenreCreate, GenreUpdate
from .base import ServiceBase


class GenreService(ServiceBase[Genre, GenreCreate, GenreUpdate]):
    pass


genre_service = GenreService(Genre)