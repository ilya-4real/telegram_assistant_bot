import aiohttp
from config import WEATHER_API_URL
from .abstract_poller import AbstractApiPoller
from json import loads


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
                    return weather
                except:
                    return None

    @staticmethod            
    def convert_to_dict(weather_data: str):
        return loads(weather_data)

