import re

from database.repositories.users import UsersRepository


class UsersService:
    repository = UsersRepository()

    @classmethod
    async def add_user(cls, user_id: int, username: str):
        result = await cls.repository.add_one(id=user_id, username=username)

    @classmethod
    async def check_email(cls, user_id: int):
        result = await cls.repository.get_user(user_id)
        return result.email
    
    @classmethod
    async def set_email(cls,user_id: int, email: str) -> None:
        await cls.repository.update_email(user_id, email)

    @classmethod
    async def set_city(cls, user_id: int, city: str):
        result = await cls.repository.update_city(user_id, city)

    @classmethod
    async def get_city(cls, user_id: int):
        user =  await cls.repository.get_user(user_id)
        return user.city
    
    @classmethod
    async def get_user(cls, user_id: int):
        return await cls.repository.get_user(user_id)
    