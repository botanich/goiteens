from typing import Optional

from sqlalchemy import Date, Column, Time, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .user import User


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    date = Column("date", Date)
    time = Column("time", Time, nullable=True)
    header: Mapped[str] = mapped_column(String(80))
    describe: Mapped[str] = mapped_column(String(240))
    user: Mapped[User] = relationship(back_populates="events")

    def __repr__(self):
        return F"Event: {self.header}"
    
    def __str__(self):
        return self.header.capitalize()
