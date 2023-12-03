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


class TasksRepository(SQLAlchemyRepository):
    model = Task

