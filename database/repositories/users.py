from .repository import SQLAlchemyRepository
from ..models import User


class UsersRepository(SQLAlchemyRepository):
    model = User

    async def update_email(self, id: int, email: str) -> None:
        await self.update_field(self.model.id, id, self.model.email, email=email)

    async def update_city(self, id: int, city: str) -> None:
        await self.update_field(self.model.id, id, self.model.city, city=city)

    async def get_user(self, user_id: int) -> User:
        result = await self.get_one(self.model.id, user_id)
        return result
