from abc import ABC, abstractmethod

from sqlalchemy import insert, select
from ..database import async_session_maker



class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError
    
    async def get_one():
        raise NotImplementedError
    

class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, id, username):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(id=id, username=username).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res
        
    async def get_one(self, id:int):
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.c.id == id)
            res = await session.execute(query)
            return res
        