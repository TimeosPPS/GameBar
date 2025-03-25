from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from .base import Base
from flask_login import UserMixin

class User(Base, UserMixin):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[Optional[str]] = mapped_column(String(50), unique=True)
    password: Mapped[Optional[str]] = mapped_column()

    def __repr__(self):
        return f"User: {self.nickname}"

    def __str__(self):
        return self.nickname.capitalize()
