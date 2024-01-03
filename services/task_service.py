from database.repositories.tasks import TasksRepository
from datetime import datetime, date, time


class TaskService:
    def __init__(self) -> None:
        self.repository = TasksRepository()

    async def add_task(
            self, 
            user_id: int, 
            title: str, 
            body: str, 
            exp_date: date, 
            exp_time: time,
            job_id: str
            ) -> None:
        exp_datetime = self.combine_date_time(exp_date, exp_time)

        await self.repository.add_one(
            user_id=user_id, 
            title=title,
            job_id=job_id, 
            body=body, 
            expires_at=exp_datetime)

    async def get_all_tasks(self, limit: int, offset: int, user_id: int):
        return await self.repository.get_all_tasks(limit, offset, user_id)
    
    async def delete_task(self, task_id: int):
        await self.repository.delete_one(self.repository.model.id, task_id)

    async def get_task(self, task_id: int):
        task = await self.repository.get_one(self.repository.model.id, task_id)
        return task
    
    async def update_task(self, task_id: int, **values):
        await self.repository.update_field(self.repository.model.id,
                                           task_id, **values)
    
    @staticmethod
    def combine_date_time(exp_date: date, exp_time: time):
        return datetime.combine(exp_date, exp_time)