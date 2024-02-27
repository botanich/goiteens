from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin

from .base import Base

class User(Base, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[Optional[str]] = mapped_column()
    email: Mapped[Optional[str]] = mapped_column()
    password: Mapped[Optional[str]] = mapped_column()
    

    def __repr__(self):
        return f"User: {self.nickname}"
    
    def __str__(self):
        return self.nickname.capitalize()
