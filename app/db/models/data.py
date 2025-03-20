from . import Base
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import mapped_column, Mapped, declarative_base

class GameBarDB(Base):
    __tablename__ = 'GameBar'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    genre: Mapped[str] = mapped_column(Text)
    rating: Mapped[int] = mapped_column(Integer)
    picture: Mapped[str] = mapped_column(Text)

class UserRecs(Base):
    __tablename__ = 'UserRec'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user: Mapped[str] = mapped_column(Text)
    genre: Mapped[str] = mapped_column(Text)
