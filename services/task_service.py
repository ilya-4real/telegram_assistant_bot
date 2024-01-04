from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from aiogram.types import Message

from database.repositories.tasks import TasksRepository
from datetime import datetime, date, time

scheduler = AsyncIOScheduler()


class TaskScheduleService:
    """Service that manages work with Apscheduler"""
    def __init__(self, scheduler: AsyncIOScheduler) -> None:
        self.scheduler = scheduler

    @staticmethod
    async def send_task_notification(bot: Bot, chat_id: int, task_title: str) -> None:
        """sends message with task notification to the chat"""
        msg = f'Your task "{task_title}" is about to expire! Do not forget about it!'
        await bot.send_message(chat_id, msg)

    def set_job(
        self, date_time: datetime, bot: Bot, chat_id: int, task_title: str
    ) -> str:
        """creates job and sets provided time, returns job id"""
        job = self.scheduler.add_job(
            self.send_task_notification,
            "date",
            run_date=date_time,
            kwargs={"bot": bot, "chat_id": chat_id, "task_title": task_title},
        )
        return job.id

    def change_job_time(self, job_id: str, date_time: datetime):
        """changes job time in scheduler"""
        self.scheduler.reschedule_job(job_id, trigger='date', run_date=date_time)

    def remove_job(self, job_id: str):
        """removes job from scheduler"""
        scheduler.remove_job(job_id)


class TaskService:
    """Manages task repository work and scheduling tasks"""
    repository = TasksRepository()
    task_scheduler = TaskScheduleService(scheduler)
    
    async def add_task(
            self, 
            user_id: int,
            message: Message, 
            title: str, 
            body: str, 
            exp_date: date, 
            exp_time: time,
            ) -> None:
        """adds new task to the database and scheduler"""
        exp_datetime = self.combine_date_time(exp_date, exp_time)
        job_id = self.task_scheduler.set_job(exp_datetime, 
                                             message.bot, message.chat.id, title)
        await self.repository.add_one(
            user_id=user_id, 
            title=title,
            job_id=job_id, 
            body=body, 
            expires_at=exp_datetime)

    async def get_all_tasks(self, limit: int, offset: int, user_id: int):
        """return tasks ordered by expiration datetime with limit and offset"""
        return await self.repository.get_all_tasks(limit, offset, user_id)
    
    async def delete_task(self, task_id: int):
        """deletes task from database and scheduler"""
        job_id = await self.repository.delete_task(task_id)
        self.task_scheduler.remove_job(job_id)
        

    async def get_task(self, task_id: int):
        """returns one task from database"""
        task = await self.repository.get_one(self.repository.model.id, task_id)
        return task
    
    async def update_task_title(self, task_id: int, title: str):
        """updates task title in database returns new one"""
        return await self.repository.update_task_field('title', task_id, title)
        
    async def update_task_desc(self, task_id: int, description: str):
        """updates task description in database returns new one"""
        return await self.repository.update_task_field('description', task_id, description)
    
    async def reschedule_task(self, task_id: int, new_date: date, new_time: time):
        """updates task expiration time in database and reschedules it in scheduler"""
        new_datetime = self.combine_date_time(new_date, new_time)
        job_id = await self.repository.update_task_expdate(task_id, new_datetime)
        self.task_scheduler.change_job_time(job_id, new_datetime)
    
    @staticmethod
    def combine_date_time(exp_date: date, exp_time: time):
        """combines date and time and returns datetime"""
        return datetime.combine(exp_date, exp_time)
