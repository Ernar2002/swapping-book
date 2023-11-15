from typing import List
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from exceptions import BadRequestException
from models import User
from schemas import UserCreate, UserUpdate
from .base import ServiceBase


class UserService(ServiceBase[User, UserCreate, UserUpdate]):
    
    def get_by_email(self, db: Session, email: str) -> User:
        return db.query(User).filter(
            User.email == email
        ).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(self.model).filter(
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: UserCreate) -> User:
        obj_in_data = jsonable_encoder(obj_in)
        user = self.model(**obj_in_data)
        
        db.add(user)
        db.flush()
        
        return user
    
    def set_discount(self, db: Session, user_id: str, discount: int):
        user = self.get_by_id(db, user_id)
        
        self.__validate_discount(discount)
        
        user.discount = discount
        
        db.add(user)
        db.flush()
        
        return user
    
    def __validate_discount(self, discount: int):
        if discount < 0 or discount > 100:
            raise BadRequestException("Discount must be between 0 and 100")

user_service = UserService(User)