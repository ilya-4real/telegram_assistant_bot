from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, BigInteger, Boolean, String, TIMESTAMP

from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users_table"
    id = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=False, default="unknown")
    registered_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    is_verified = Column(Boolean, nullable=False, default=False)