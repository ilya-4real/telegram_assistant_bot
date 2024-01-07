from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
import sys
from aiogram.types import Update

from config import API_KEY, LOCAL_IP
from bot import bot, dp, routers


WEBHOOK_PATH =f'/bot/{API_KEY}' 
WEBHOOK_URl = LOCAL_IP + WEBHOOK_PATH

dp.include_routers(*routers)


@asynccontextmanager
async def lifespan(app: FastAPI):
    #on startup
    async with bot.session:
        webhook_info = await bot.get_webhook_info()
        if webhook_info.url != WEBHOOK_URl:
            logging.basicConfig(level=logging.INFO, stream=sys.stdout)
            await bot.set_webhook(WEBHOOK_URl)
        yield
        #on shutdown
    

app = FastAPI(lifespan=lifespan)

@app.post(WEBHOOK_PATH)
async def webhook(update: Update):
    responce = await dp.feed_webhook_update(bot, update)
    return responce

