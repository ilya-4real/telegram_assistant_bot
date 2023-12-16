from pyexpat import model
from .utils.repository import SQLAlchemyRepository
from .models import User, Task
from .database import async_session_maker
from sqlalchemy import insert, select, update


class UsersRepository(SQLAlchemyRepository):
    model = User

    async def set_email(self, id, email):
        async with async_session_maker() as session:
            current_user = await session.get(self.model, id)
            current_user.email = email
            await session.commit()

    async def set_city(self, id, city):
        async with async_session_maker() as session:
            current_user = await session.get(self.model, id)
            current_user.city = city
            await session.commit()

    async def get_email(self, user_id: int):
        async with async_session_maker() as session:
            query = select(self.model.email).where(self.model.id == user_id)
            email = await session.execute(query)
            return email.scalar_one_or_none()
        
    async def get_city(self, user_id: int):
        async with async_session_maker() as session:
            query = select(self.model.city).where(self.model.id == user_id)
            email = await session.execute(query)
            return email.scalar_one_or_none()
