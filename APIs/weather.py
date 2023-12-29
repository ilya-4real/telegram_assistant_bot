import aiohttp
from config import WEATHER_API_URL
from .abstract_poller import AbstractApiPoller
from json import loads
from .exceptions import InvalidCity


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
                if weather.get('error'):
                    raise InvalidCity("There is no weather for your city")
                return weather

    @staticmethod            
    def convert_to_dict(weather_data: str):
        return loads(weather_data)

