import aiohttp
from config import CURRENCIES_API_URL, CURRENCIES_KEY
from .abstract_poller import AbstractApiPoller
from app.exceptions import InvalidCurrencies


class CurrencyApiPoller(AbstractApiPoller):
    """manages polling data from currency API"""
    url = CURRENCIES_API_URL
    key = CURRENCIES_KEY

    @classmethod
    async def poll_data(cls, symbols: str) -> dict[str, float]:
        """actually polls data about provided symbols they should be in format like 'USD,EUR,BTC'"""
        params = {
            'access_key': cls.key,
            'symbols': symbols
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(cls.url, params=params) as responce:
                currencies = await responce.json()
                if responce.status != 200:
                    raise InvalidCurrencies("Bad currency symbol")
                return currencies['rates']
