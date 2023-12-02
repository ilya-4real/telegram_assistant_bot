from .utils.repository import SQLAlchemyRepository
from .models import User
from .database import async_session_maker
from sqlalchemy import insert, select, update


class UsersRepository(SQLAlchemyRepository):
    model = User

    async def add_user_email(self, id, email):
        async with async_session_maker() as session:
            current_user = await session.get(self.model, id)
            current_user.email = email
            await session.commit()
