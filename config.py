from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get("API_KEY")
WEATHER_KEY = os.environ.get("WEATHER_API_KEY")

WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"

cities = {
    "kaliningrad": (54.7, 20.5),
}
