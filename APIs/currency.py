import aiohttp
from config import CURRENCIES_API_URL, CURRENCIES_KEY
from .abstract_poller import AbstractApiPoller
from exceptions import InvalidCurrencies


class CurrencyApiPoller(AbstractApiPoller):
    def __init__(self, key) -> None:
        self.url = CURRENCIES_API_URL
        self.key = key

    async def poll_data(self, symbols: str) -> dict[str, float]:
        params = {
            'access_key': self.key,
            'symbols': symbols
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, params=params) as responce:
                currencies = await responce.json()
                if currencies.get('error'):
                    raise InvalidCurrencies("Bad currency symbol")
                return currencies['rates']
