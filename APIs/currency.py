import aiohttp
from config import CURRENCIES_API_URL
from .abstract_poller import AbstractApiPoller


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
                try:
                    return currencies['rates']
                except:
                    return None
