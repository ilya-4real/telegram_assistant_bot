import re

from app.APIs import ApisData, FacadeApiGateway
from app.database.repositories.users import UsersRepository
from app.database.repositories.currencies import CurrencyRepository
from app.database.models import CurrencySymbol
from app.exceptions import InvalidCurrencies


class CurrencyService:
    """Service that manages currency API accesses and database reads"""
    def __init__(self) -> None:
        self.repository = CurrencyRepository()

    def check_currency_symbol(self, symbol: str) -> str | None:
        """checks is provided symbol correct or net with regex"""
        result = re.search(r'^[a-zA-Z]{3}$', symbol)
        return symbol.upper() if result else None

    async def add_currency_to_user(self, symbol: str, user_id):
        """adds currensy symbol to users table in database"""
        await self.repository.add_one(symbol=symbol, user_id=user_id)

    async def get_currency_rates(self, user_id: int) -> dict[str, float]:
        """returns currency symbols rates from API"""
        symbols = await self.get_user_currency_symbols(user_id)
        if not symbols:
            raise InvalidCurrencies("Please, set your currencies using /add_currency or remove incorrect /delete_currency")
        result = await FacadeApiGateway.get_currencies(symbols)
        return result

    async def get_user_currency_symbols(self, user_id: int):
        """returns user's currency symbols from database"""
        symbols = await self.repository.get_symbols(user_id)
        string_of_symbols = self.convert_to_string(symbols)
        return string_of_symbols
    
    async def delete_currency_by_symbol(self, symbol: str, user_id: int):
        """deletes one currency symbol from database"""
        await self.repository.delete_by_symbol(symbol, user_id)
    
    @staticmethod
    def convert_to_string(symbols: list[CurrencySymbol]):
        """converts database symbols to string like: 'USD,RUB,EUR'"""
        res = []
        for symbol in symbols:
            res.append(symbol.symbol)
        return ','.join(res)
    

class WeatherService:
    """Service that accesses weather API and database"""
    def __init__(self) -> None:
        self.api_gateway = FacadeApiGateway
        self.repository = UsersRepository()

    async def get_weather(self, user_id: int):
        """returns current weather from API"""
        user = await self.repository.get_user(user_id)
        weather = await self.api_gateway.get_weather(user.city)
        return weather
