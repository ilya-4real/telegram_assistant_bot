from .currency import CurrencyApiPoller
from .weather import WeatherApiPoller
from config import WEATHER_KEY, CURRENCIES_KEY

class FacadeApiGateway:
    def __init__(self, city: str) -> None:
        self.weather_poller = WeatherApiPoller(WEATHER_KEY, q=city, units='metric')
        # self.currency_poller = CurrencyApiPoller(CURRENCIES_KEY, symbols=','.join(curencies))

    async def get_apis_data(self):
        weather = await self.weather_poller.poll_data()
        currency_rates = await self.currency_poller.poll_data()
        result = {
            "weather": weather,
            "currency_rates": currency_rates
        }
        return result
    
    async def get_weather(self) -> dict:
        weather = await self.weather_poller.poll_data()
        return weather
    
    async def get_currencies(self) -> dict:
        rates = await self.currency_poller.poll_data()
        return {"rates": rates}

