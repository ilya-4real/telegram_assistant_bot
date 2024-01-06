import re

from app.database.repositories.users import UsersRepository
from app.config import ADMIN_ID


class UsersService:
    """Service that manages work with user and it's database table"""
    repository = UsersRepository()

    @classmethod
    async def add_user(cls, user_id: int, username: str):
        """adds new user to database"""
        result = await cls.repository.add_one(id=user_id, username=username)

    @classmethod
    async def check_email(cls, user_id: int):
        """returns user email if it is set"""
        result = await cls.repository.get_user(user_id)
        return result.email
    
    @classmethod
    def check_is_admin(cls, user_id: int):
        """returns True if user is admin"""
        return user_id == int(ADMIN_ID)
    
    @classmethod
    async def set_email(cls,user_id: int, email: str) -> None:
        """sets user's email in database"""
        await cls.repository.update_email(user_id, email)

    @classmethod
    async def set_city(cls, user_id: int, city: str):
        """sets user's city in database"""
        result = await cls.repository.update_city(user_id, city)

    @classmethod
    async def get_city(cls, user_id: int):
        """returns user's city from database if exists"""
        user =  await cls.repository.get_user(user_id)
        return user.city
    
    @classmethod
    async def get_user(cls, user_id: int):
        """returns user model from database"""
        return await cls.repository.get_user(user_id)
    