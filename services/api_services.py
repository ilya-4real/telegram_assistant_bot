import re

from APIs import api_gate, ApisData
from database.repositories.users import UsersRepository
from database.repositories.currencies import CurrencyRepository
from database.models import CurrencySymbol
from exceptions import UserCurrencyNotSet


class CurrencyService:
    """Service that manages currency API accesses and database reads"""
    def __init__(self) -> None:
        self.repository = CurrencyRepository()

    def check_currency_symbol(self, symbol: str) -> str | None:
        result = re.search(r'^[a-zA-Z]{3}$', symbol)
        return symbol.upper() if result else None

    async def add_currency_to_user(self, symbol: str, user_id):
        await self.repository.add_one(symbol=symbol, user_id=user_id)

    async def get_currency_rates(self, user_id: int):
        symbols = await self.get_user_currency_symbols(user_id)
        if not symbols:
            raise UserCurrencyNotSet("Please, set your currencies using /add_currency")
        result = await api_gate.FacadeApiGateway().get_currencies(symbols)
        return result

    async def get_user_currency_symbols(self, user_id: int):
        symbols = await self.repository.get_symbols(user_id)
        string_of_symbols = self.convert_to_string(symbols)
        return string_of_symbols
    
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
        self.api_gateway = api_gate.FacadeApiGateway()
        self.repository = UsersRepository()

    async def get_weather(self, user_id: int):
        user = await self.repository.get_user(user_id)
        weather = await self.api_gateway.get_weather(user.city)
        return weather
    

class InfoService:
    """Service that Manages both weather and currency API"""
    def __init__(self) -> None:
        self.user_repository = UsersRepository()
        self.currency_repository = CurrencyRepository()
        self.api_gateway = api_gate.FacadeApiGateway()
    
    async def get_info(self, user_id: int) -> ApisData:
        user = await self.user_repository.get_user(user_id)
        cur_syms = await self.currency_repository.get_symbols(user_id)
        converted_cur_syms = ','.join([symbol.symbol for symbol in cur_syms])
        info = await self.api_gateway.get_apis_data(user.city, converted_cur_syms)
        return info
