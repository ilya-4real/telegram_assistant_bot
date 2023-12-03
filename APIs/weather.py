import aiohttp
from config import WEATHER_KEY, WEATHER_API_URL, cities
import asyncio

coords = cities.get('kaliningrad')

async def get_weather():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            WEATHER_API_URL.format(
            lat=coords[0], 
            lon=coords[1], 
            API_KEY=WEATHER_KEY
            )
            ) as responce:
            print(responce.status)
            weather = await responce.json()
            try:
                return weather['main']['temp']-273
            except:
                return None

async def main():
    weather_task = asyncio.create_task(get_weather())
    await weather_task


if __name__ =="__main__":
    asyncio.run(main())