from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, ForeignKey
from .database import Base

from datetime import datetime
from typing import Annotated


pk = Annotated[int, mapped_column(BigInteger, primary_key=True)]

class User(Base):
    __tablename__ = "users_table"
    id: Mapped[pk]
    username: Mapped[str] = mapped_column(nullable=False, default="unknown")
    email: Mapped[str | None]
    registered_at: Mapped[datetime] = mapped_column(
        nullable=False, 
        default=datetime.utcnow
        )
    city: Mapped[str | None]
    is_admin: Mapped[bool] = mapped_column(default=False)


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str | None]
    body: Mapped[str | None]
    created_at : Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    expires_at : Mapped[datetime | None]
    job_id: Mapped[str] 
    user_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete="CASCADE"))


class Image(Base):
    __tablename__ = "images"
    tg_id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)


class CurrencySymbol(Base):
    __tablename__ = "currency_symbols"
    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users_table.id", ondelete="CASCADE"))
