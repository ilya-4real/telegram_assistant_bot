from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import delete, insert, select, update

from database.models import User
from ..database import async_session_maker
from sqlalchemy.exc import IntegrityError


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self):
        raise NotImplementedError

    async def get_one(self):
        raise NotImplementedError

    async def delete_one(self):
        raise NotImplementedError

    async def get_all(self):
        raise NotImplementedError

    async def update_field(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, **data):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(data)
            await session.execute(stmt)
            await session.commit()

    async def get_one(self, filter, filter_value):
        async with async_session_maker() as session:
            query = select(self.model).where(filter == filter_value)
            res = await session.execute(query)
            return res.scalar_one_or_none()

    async def delete_one(self, filter, filter_value, returning_field):
        async with async_session_maker() as session:
            stmt = (
                delete(self.model)
                .where(filter == filter_value)
                .returning(returning_field)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar()

    async def get_all(self, limit: int, offset: int):
        async with async_session_maker() as session: 
            query = select(self.model).limit(limit).offset(offset)
            res = await session.execute(query)
            return res.scalars().all()

    async def update_field(self, filter: Any, filter_value: Any,
                            return_field: Any, **values: Any):
        async with async_session_maker() as session:
            stmt = (
                update(self.model)
                .where(filter == filter_value)
                .values(**values)
                .returning(return_field)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()


class SQLAlchemyOneToManyRepository(SQLAlchemyRepository):
    model = User
    foreign_model = None

    async def select_related(
            self,
            limit: int,
            offset: int,
            order_by: Any,
            filter: Any,
            filter_value:
            Any):
        
        async with async_session_maker() as session:
            query = (
                select(self.model)
                .join(self.foreign_model)
                .where(filter == filter_value)
                .order_by(order_by)
                .limit(limit)
                .offset(offset)
            )
            res = await session.execute(query)
            return res.scalars().all()
