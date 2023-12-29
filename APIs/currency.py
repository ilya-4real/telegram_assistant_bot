import aiohttp
from config import CURRENCIES_API_URL, CURRENCIES_KEY
from .abstract_poller import AbstractApiPoller
from .exceptions import InvalidCurrencies


class CurrencyApiPoller(AbstractApiPoller):
    def __init__(self) -> None:
        self.url = CURRENCIES_API_URL
        self.params = {
            "access_key": CURRENCIES_KEY,
        }

    async def poll_data(self, symbols: str) -> dict[str, float]:
        self.params['symbols'] = symbols
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, params=self.params) as responce:
                currencies = await responce.json()
                if currencies.get('error'):
                    raise InvalidCurrencies("Bad currency symbol")
                return currencies['rates']
