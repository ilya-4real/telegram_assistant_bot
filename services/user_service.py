from database.repositories.users import UsersRepository


class UsersService:
    def __init__(self) -> None:
        self.repository = UsersRepository()

    async def add_user(self, user_id: int, username: str):
        result = await self.repository.add_one(id=user_id, username=username)

    async def check_email(self, user_id: int):
        result = await self.repository.get_user(user_id)
        return result.email
    
    async def set_city(self, user_id: int, city: str):
        result = await self.repository.update_city(user_id, city)

    async def get_city(self, user_id: int):
        user =  await self.repository.get_user(user_id)
        return user.city
    
    async def get_user(self, user_id: int):
        return await self.repository.get_user(user_id)
    
