import aiohttp
from config import CURRENCIES_API_URL, CURRENCIES_KEY


async def get_currency():
    async with aiohttp.ClientSession() as session:
        url = CURRENCIES_API_URL.format(CURRENCIES_KEY)
        async with session.get(url) as responce:
            currencies = await responce.json()
            try:
                return currencies['rates']
            except:
                return None
