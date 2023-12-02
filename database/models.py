from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, text
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
    is_verified: Mapped[bool] = mapped_column(nullable=False, default=False)
