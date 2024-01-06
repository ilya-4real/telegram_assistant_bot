from .repository import SQLAlchemyOneToManyRepository
from ..models import CurrencySymbol, User


class CurrencyRepository(SQLAlchemyOneToManyRepository):
    """Repo for currency model in database"""

    model = CurrencySymbol
    foreign_model = User

    async def get_symbols(self, user_id: int):
        """get all symbols associated with user"""
        result = await self.select_related(
            5, 0, self.model.id, self.foreign_model.id, user_id
        )
        return result

    async def delete_by_symbol(self, symbol: str, user_id):
        """delete specific symbol from database"""
        await self.delete_related(
            self.model.user_id, user_id, self.model.symbol, symbol
        )
