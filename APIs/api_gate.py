from .currency import CurrencyApiPoller
from .weather import WeatherApiPoller
from config import WEATHER_KEY, CURRENCIES_KEY

from typing import NamedTuple

class ApisData(NamedTuple):
    weather: dict[str, str | float]
    currency: dict[str, str | float]


class FacadeApiGateway:
    def __init__(self) -> None:
        self.weather_poller = WeatherApiPoller(WEATHER_KEY)
        self.currency_poller = CurrencyApiPoller(CURRENCIES_KEY)

    async def get_apis_data(self, city: str, currency_symbols: str) -> ApisData:
        weather = await self.weather_poller.poll_data(units='metric', q=city)
        currency_rates = await self.currency_poller.poll_data(currency_symbols)
        return ApisData(weather, currency_rates)

    async def get_weather(self, city: str) -> dict[str, float]:
        weather = await self.weather_poller.poll_data(units='metric', q=city)
        return weather

    async def get_currencies(self, symbols: str) -> dict[str, str | float]:
        rates = await self.currency_poller.poll_data(symbols)
        return rates
