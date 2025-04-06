# app/utils/check_subscription.py

from aiogram import Bot
from app.data.channels import CHANNELS

async def check_user_subscriptions(bot: Bot, user_id: int):
    unsubscribed = []

    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel["username"], user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                unsubscribed.append(channel)
        except Exception:
            unsubscribed.append(channel)

    return unsubscribed
