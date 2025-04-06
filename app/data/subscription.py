# app/filters/subscription.py

from aiogram import Bot
from aiogram.types import Message
from aiogram.filters import BaseFilter
from app.data.check_subscription import check_user_subscriptions

class IsSubscribed(BaseFilter):
    async def __call__(self, message: Message, bot: Bot):
        unsubscribed = await check_user_subscriptions(bot, message.from_user.id)
        return len(unsubscribed) == 0
