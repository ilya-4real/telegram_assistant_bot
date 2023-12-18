from .repository import SQLAlchemyRepository, SQLAlchemyOneToManyRepository
from ..models import Task, User

class TasksRepository(SQLAlchemyOneToManyRepository):
    model = Task
    foreign_model = User

    async def get_all(self, limit: int, offset: int, user_id: int):
        return await self.select_related(
            limit, 
            offset, 
            self.model.expires_at, 
            self.foreign_model.id, 
            user_id
            )