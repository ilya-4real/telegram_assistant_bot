from .repository import SQLAlchemyOneToManyRepository
from ..models import CurrencySymbol, User

class CurrencyRepository(SQLAlchemyOneToManyRepository):
    model = CurrencySymbol
    foreign_model = User

    async def get_symbols(self, user_id: int):
        result = await self.select_related(5, 0, self.model.id, self.foreign_model.id, user_id)
        return result