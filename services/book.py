from typing import Any, Dict, Union
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from fastapi.encoders import jsonable_encoder

from models import Book, Author, Genre
from schemas import BookCreate, BookUpdate
from .base import ServiceBase
from .author import author_service
from .genre import genre_service
from .user import user_service


class BookService(ServiceBase[Book, BookCreate, BookUpdate]):
    
    def get_all(self,
                db: Session,
                filter: str = None,
                sort_field: str = None,
                sort_order: str = 'asc',
                skip: int = 0,
                limit: int = 100):
        
        query = (
            db.query(self.model)
                .join(Author, self.model.author_id == Author.id)
                .join(Genre, self.model.genre_id == Genre.id)
                .filter(self.model.is_active == True)
        )
        
        if filter: 
            query = self.__search(query, filter)
               
        if sort_field:
            query = self.__sort(query, sort_field, sort_order)
        
        return query.offset(skip).limit(limit).all()
        
    def get_by_user(self,
                    db: Session,
                    user_id: str,
                    filter: str = None,
                    sort_field: str = None,
                    sort_order: str = 'asc',
                    skip: int = 0,
                    limit: int = 100):
        user_service.get_by_id(db, user_id)
        
        query = (
            db.query(self.model)
                .join(Author, self.model.author_id == Author.id)
                .join(Genre, self.model.genre_id == Genre.id)
                .filter(
                    self.model.publisher_id == user_id,
                    self.model.is_active == True
                )
        )
        
        if filter:
            query = self.__search(query, filter)
               
        if sort_field:
            query = self.__sort(query, sort_field, sort_order)
        
        return query.offset(skip).limit(limit).all()
    
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
        
    def __search(self, query, filter: str):
        return (
            query
                .filter(
                    self.model.name.ilike(f'%{filter}%') |
                    Author.name.ilike(f'%{filter}%') |
                    Genre.name.ilike(f'%{filter}%')
                )
        )
    
    def __sort(self, query, sort_field: str, sort_order: str):
        order = desc if sort_order == 'desc' else asc
        if sort_field == 'book':
            query = query.order_by(order(self.model.name))
        elif sort_field == 'author':
            query = (
                query.order_by(order(Author.name))
            )
        elif sort_field == 'genre':
            query = (
                query.order_by(order(Genre.name))
            )
            
        return query
        
        

book_service = BookService(Book)