from typing import Literal
import aiohttp
from json import loads

from app.exceptions import InvalidCity
from config import WEATHER_API_URL, WEATHER_KEY
from .abstract_poller import AbstractApiPoller


class WeatherApiPoller(AbstractApiPoller):
    """ "weather API poller"""

    url = WEATHER_API_URL
    key = WEATHER_KEY

    @classmethod
    async def poll_data(
        cls, city: str, units: Literal["standard", "metric", "imperial"]
    ) -> dict[str, str | float]:
        """actually poll data from API city should be in format like 'New-York'"""
        params = {"appid": cls.key, "q": city, "units": units}
        async with aiohttp.ClientSession() as session:
            async with session.get(cls.url, params=params) as responce:
                weather = await responce.json()
                if responce.status != 200:
                    raise InvalidCity("There is no weather for your city")
                return weather
