import asyncio
from aiogram import Dispatcher, Bot

from app import handlers as hls

bot= Bot(token="7710418619:AAHsTjz0AM7JvUXmXgmi1YF2EmZMgwgHZeg")

async def run():
    dp= Dispatcher()
    dp.include_router(hls.router)
    await dp.start_polling(bot)

if __name__=='__main__':
    asyncio.run(run())