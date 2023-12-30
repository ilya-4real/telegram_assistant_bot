import aiohttp
from config import WEATHER_API_URL
from .abstract_poller import AbstractApiPoller
from json import loads
from .exceptions import InvalidCity


class WeatherApiPoller(AbstractApiPoller):
    def __init__(self, key) -> None:
        self.url = WEATHER_API_URL
        self.key = key

    async def poll_data(self, **query_params: str) -> dict[str, str | float]:
        params = {
            "appid": self.key,
            **query_params
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, params=params) as responce:
                print(responce.status)
                weather = await responce.json()
                if weather.get('error'):
                    raise InvalidCity("There is no weather for your city")
                return weather

    @staticmethod            
    def convert_to_dict(weather_data: str):
        return loads(weather_data)

