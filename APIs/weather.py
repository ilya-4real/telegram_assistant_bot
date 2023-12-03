import aiohttp
from config import WEATHER_API_URL
from abstract_poller import AbstractApiPoller


class WeatherApiPoller(AbstractApiPoller):
    def __init__(self, key, **params) -> None:
        self.url = WEATHER_API_URL
        self.params = {
            "appid": key,
            **params
        }

    async def poll_data(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, params=self.params) as responce:
                print(responce.status)
                weather = await responce.json()
                try:
                    return weather['main']['temp']-273
                except:
                    return None

