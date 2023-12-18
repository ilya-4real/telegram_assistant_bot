import aiohttp
from config import CURRENCIES_API_URL
from .abstract_poller import AbstractApiPoller
from .exceptions import InvalidCurrencies


class CurrencyApiPoller(AbstractApiPoller):
    def __init__(self, key, **params) -> None:
        self.url = CURRENCIES_API_URL
        self.params = {
            "access_key": key,
            **params
        }
    async def poll_data(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, params=self.params) as responce:
                currencies = await responce.json()
                if not currencies:
                    raise InvalidCurrencies("Bad currency symbol")
                return currencies['rates']