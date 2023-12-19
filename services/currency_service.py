from database.repositories.currencies import CurrencyRepository
from database.models import CurrencySymbol
from APIs.api_gate import FacadeApiGateway
import re


class CurrencyService:
    def __init__(self) -> None:
        self.repository = CurrencyRepository()

    def check_currency_symbol(self, symbol: str) -> str | None:
        result = re.search(r'^[a-zA-Z]{3}$', symbol)
        return symbol.upper() if result else None
    
    async def add_currency_to_user(self, symbol: str, user_id): 
        await self.repository.add_one(symbol=symbol, user_id=user_id)

    async def get_user_symbols(self, user_id: int) -> list[str]:
        symbols = await self.repository.get_symbols(user_id)
        return self.convert_to_list_of_strings(symbols)
    
    async def get_currency_rates(self, user_id: int):
        symbols = await self.repository.get_symbols(user_id)
        list_of_symbols = self.convert_to_list_of_strings(symbols)
        result = await FacadeApiGateway().get_currencies(list_of_symbols)
        return result
        

    @staticmethod
    def convert_to_list_of_strings(symbols: list[CurrencySymbol]):
        res = []
        for symbol in symbols:
            res.append(symbol.symbol)
        return res
        