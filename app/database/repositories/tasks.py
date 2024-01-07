from typing import Literal
from datetime import datetime

from .repository import SQLAlchemyOneToManyRepository
from ..models import Task, User


class TasksRepository(SQLAlchemyOneToManyRepository):
    model = Task
    foreign_model = User

    async def get_all_tasks(self, limit: int, offset: int, user_id: int) -> list[Task]:
        """returns all tasks with provided limit and offset"""
        return await self.select_related(
            limit, offset, self.model.expires_at, self.foreign_model.id, user_id
        )

    async def update_task_field(
        self, field_name: Literal["description", "title"], task_id: int, value: str
    ) -> str:
        """updates one column in one task row"""
        match field_name:
            case "description":
                result = await self.update_field(
                    self.model.id, task_id, self.model.body, body=value
                )
            case "title":
                result = await self.update_field(
                    self.model.id, task_id, self.model.title, title=value
                )
        return result

    async def update_task_expdate(self, task_id: int, exp_datetime: datetime) -> str:
        """updates expiration date in task model"""
        job_id = await self.update_field(
            self.model.id, task_id, self.model.job_id, expires_at=exp_datetime
        )
        return job_id

    async def delete_task(self, task_id: int) -> str:
        return await self.delete_one(self.model.id, task_id, self.model.job_id)
