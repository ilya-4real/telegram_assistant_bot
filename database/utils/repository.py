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

    async def add_one(self, id):
        async with async_session_maker() as session:
            session.add(self.model(id=id))
            try:
                await session.commit()
            except IntegrityError:
                query = select(self.model.id)
                res = await session.execute(query)
            return res
        
    async def get_one(self, id:int):
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.c.id == id)
            res = await session.execute(query)
            return res
        