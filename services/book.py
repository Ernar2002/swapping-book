from typing import Any, Dict, Union
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from models import Book
from schemas import BookCreate, BookUpdate
from .base import ServiceBase
from .author import author_service
from .genre import genre_service
from .user import user_service


class BookService(ServiceBase[Book, BookCreate, BookUpdate]):
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter(
            self.model.is_active == True,
        ).offset(skip).limit(limit).all()
        
    def get_by_user(self, db: Session, user_id: str, skip: int = 0, limit: int = 100):
        user_service.get_by_id(db, user_id)
        
        return db.query(self.model).filter(
            self.model.publisher_id == user_id,
            self.model.is_active == True,
        ).offset(skip).limit(limit).all()
    
    def delete(self, db: Session, id: str):
        book = self.get_by_id(db, id)
        book.is_active = False
        
        db.add(book)
        db.flush()
        
        return book
    
    def create(self, db: Session, obj_in: BookCreate, user_id: str) -> Book:
        self.__validate_foreign_keys(db, user_id, obj_in.genre_id, obj_in.author_id)
        
        obj_in_data = jsonable_encoder(obj_in)
        book = self.model(**obj_in_data)
        book.publisher_id = user_id
        
        db.add(book)
        db.flush()
        
        return book
    
    def __validate_foreign_keys(self,
                                db: Session,
                                user_id: str,
                                genre_id: str,
                                author_id: str):
        user_service.get_by_id(db, user_id)
        genre_service.get_by_id(db, genre_id)
        author_service.get_by_id(db, author_id)

book_service = BookService(Book)