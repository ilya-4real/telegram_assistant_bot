from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.job import Job
from aiogram import Bot


class ApschedulerService:
    def __init__(self, scheduler: AsyncIOScheduler) -> None:
        self.scheduler = scheduler

    @staticmethod
    async def send_task_notification(bot: Bot, chat_id: int, task_title: str) -> None:
        msg = f'Your task "{task_title}" is about to expire! Do not forget about it!'
        await bot.send_message(chat_id, msg)

    async def set_job(self, date_time: datetime, bot: Bot, chat_id: int , task_title: str) -> str:
        """creates job and sets provided time, returns job id"""
        job = self.scheduler.add_job(
            self.send_task_notification, 
            'date', 
            run_date=date_time, 
            kwargs={'bot': bot, 'chat_id': chat_id, 'task_title': task_title}
            )
        return job.id

    def change_job_time(self, job: Job, date_time: datetime):
        self.scheduler.modify_job(job.id, run_date=date_time)