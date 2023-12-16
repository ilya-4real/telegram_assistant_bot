from ..users import UsersRepository


class UsersService:
    def __init__(self) -> None:
        self.repository = UsersRepository()

    async def check_email(self, user_id: int):
        result = await self.repository.get_email(user_id)
        return result 
    
    async def set_city(self, user_id: int, city: str):
        result = await self.repository.set_city(user_id, city)

    async def get_city(self, user_id: int):
        result = await self.repository.get_city(user_id)
        return result
    
