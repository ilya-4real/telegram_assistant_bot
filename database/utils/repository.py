from abc import ABC, abstractmethod

from sqlalchemy import insert, select
from ..database import async_session_maker
from sqlalchemy.exc import IntegrityError



class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError
    
    async def get_one():
        raise NotImplementedError
    

class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, **data):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(data).returning(self.model.id)
            try:
                res = await session.execute(stmt)
                await session.commit()
            except IntegrityError:
                return "already exists"
            return res.one()[0]
        
    async def get_one(self, id:int):
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.id == id)
            res = await session.execute(query)
            return res.one_or_none()
        