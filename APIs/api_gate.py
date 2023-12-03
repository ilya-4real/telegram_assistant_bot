from .currency import get_currency
from .weather import get_weather

async def get_currency_and_weather():
    weather = await get_weather()
    currency_rates = await get_currency()
    result = {
        "weather": weather,
        "currency_rates": currency_rates
    }
    return result