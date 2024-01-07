from config import WEATHER_KEY, CURRENCIES_KEY
from .currency import CurrencyApiPoller
from .weather import WeatherApiPoller


from typing import NamedTuple

class ApisData(NamedTuple):
    weather: dict[str, str | float]
    currency: dict[str, str | float]


class FacadeApiGateway:
    """class that manages polling data from APIs"""
    weather_poller = WeatherApiPoller
    currency_poller = CurrencyApiPoller

    @classmethod
    async def get_weather(cls, city: str) -> dict[str, float]:
        """polls weather API"""
        weather = await cls.weather_poller.poll_data(city, 'metric')
        return weather

    @classmethod
    async def get_currencies(cls, symbols: str) -> dict[str, str | float]:
        """polls currency API"""
        rates = await cls.currency_poller.poll_data(symbols)
        return rates
