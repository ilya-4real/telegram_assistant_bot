from dotenv import load_dotenv
import os


load_dotenv()

API_KEY = os.environ.get("API_KEY")
WEATHER_KEY = os.environ.get("WEATHER_API_KEY")
CURRENCIES_KEY = os.environ.get("CURRENCY_API_KEY")

WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
CURRENCIES_API_URL = "http://api.exchangeratesapi.io/v1/latest"
