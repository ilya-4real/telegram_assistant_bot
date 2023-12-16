from ..users import UsersRepository


class UsersService:
    def __init__(self) -> None:
        self.repository = UsersRepository()

    async def check_email(self, user_id: int):
        result = await self.repository.get_email(user_id)
        return result 