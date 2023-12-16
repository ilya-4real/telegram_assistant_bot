from curses.ascii import US
from sqlalchemy import select
from .utils.repository import SQLAlchemyRepository
from .models import Task, User
from .database import async_session_maker

class TasksRepository(SQLAlchemyRepository):
    model = Task
    foreign_model = User

    async def get_all(self, limit: int, offset: int):
        async with async_session_maker() as session:
            query = (
                select(self.model)
                .join(self.foreign_model)
                .order_by(self.model.expires_at)
                .limit(limit)
                .offset(offset)
            )
            tasks = await session.execute(query)
            return tasks.scalars().all()