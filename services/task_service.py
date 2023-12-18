from database.repositories.tasks import TasksRepository
from datetime import date, time, datetime


class TaskService:
    def __init__(self) -> None:
        self.repository = TasksRepository()

    async def add_task(self, user_id: int, title: str, body: str, exp_date: date, exp_time: time):
        exp_datetime = datetime.combine(exp_date, exp_time)
        await self.repository.add_one(user_id=user_id, title=title, body=body, expires_at=exp_datetime)

    async def get_all(self, limit: int, offset: int, user_id: int):
        return await self.repository.get_all(limit, offset, user_id)
