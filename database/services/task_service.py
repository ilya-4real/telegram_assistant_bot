from .. tasks import TasksRepository
from datetime import date, time
from services.task_date_checking import to_datetime


class TaskService:
    def __init__(self) -> None:
        self.repository = TasksRepository()

    async def add_task(self, user_id: int, title: str, body: str, date: date, time: time):
        exp_datetime = to_datetime(date, time)
        await self.repository.add_one(user_id=user_id, title=title, body=body, expires_at=exp_datetime)

    async def get_all(self, user_id: int=0):
        return await self.repository.get_all()
