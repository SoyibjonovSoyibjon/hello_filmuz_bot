from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from app import keyboards as kb
from main import bot
import asyncio
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from app.data.check_subscription import check_user_subscriptions
from app.data.channels import CHANNELS
from aiogram import Bot

router= Router()
botAdmin= [7226256500, 5131171528]

@router.message(CommandStart())
async def cmd_start(message: Message):
    await asyncio.sleep(1)
    await message.answer(
        f"<strong>Assalomu alaykum @{message.from_user.username} 👋\nBotimizga xush kelibsiz 😎\nKerakli film kodini yuboring !</strong>",
        reply_markup=kb.main_kb,
        parse_mode='HTML'
    )
    for admins in botAdmin:
        await bot.send_message(
            admins,
            f"<strong>Start bosdi:\n\nName: {message.from_user.full_name}\nUsername: @{message.from_user.username},\nUser_id: {message.from_user.id}</strong>",
            parse_mode='HTML'
        )

@router.message(F.text == '/admin')
async def cmd_admin(message: Message):
    await asyncio.sleep(1)
    await message.answer(
        "Bot admini:\n<strong>@Soyibjon_2353</strong>",
        parse_mode='HTML'
    )





# Admin paneli

def is_admin(user_id: int) -> bool:
    return user_id in botAdmin

@router.message(F.text == '/admin_paneli')
async def cmd_admin_paneli(message: Message):
    # chat_member= await bot.get_chat_member(chat_id=message.chat.id, user_id= message.from_user.id)

    if message.from_user.id not in botAdmin:
        await asyncio.sleep(1)
        await message.answer("Kechirasiz ushbu buyruq faqat adminlar uchun !")
        return
    await asyncio.sleep(1)
    await message.answer("<strong>Admin paneliga o‘tdingiz !</strong>",reply_markup=kb.admin_kb , parse_mode='HTML')

@router.message(F.text == '/reklama_yuborish')
async def cmd_reklama_yuborish(message: Message):
    if is_admin(message.from_user.id):
        await asyncio.sleep(1)
        await message.answer('Reklama yuborish !')
        return
    
@router.message(F.text == '/foydalanuvchilar_soni')
async def cmd_reklama_yuborish(message: Message):
    if is_admin(message.from_user.id):
        await asyncio.sleep(1)
        await message.answer('Foydalanuvchilar sonini ko‘rish !')
        return
    



# Instagram tugmasi bosilgan user_id'larni saqlovchi to‘plam
instagram_visited_users = set()

async def check_user_subscriptions(bot: Bot, user_id: int):
    unsubscribed = []

    for channel in CHANNELS:
        if channel["type"] == "telegram":
            try:
                member = await bot.get_chat_member(chat_id=channel["username"], user_id=user_id)
                if member.status not in ['member', 'administrator', 'creator']:
                    unsubscribed.append(channel)
            except:
                unsubscribed.append(channel)
        elif channel["type"] == "instagram":
            if user_id not in instagram_visited_users:
                unsubscribed.append(channel)

    return unsubscribed



# Obunani tekshirish


# Har bir foydalanuvchi uchun oxirgi yuborilgan xabar ID sini saqlaymiz
last_messages = {}

# Foydalanuvchidan kelgan har qanday mavjud bo'lmagan buyruqlarda tekshiradi (foydalanuvchi kanallarga obuna bo'lganligini tekshirish)
@router.message()
async def cmd_any(message: Message):
    user_id = message.from_user.id
    unsubscribed = await check_user_subscriptions(bot, user_id)

    if not unsubscribed:
        await message.answer("Botga xush kelibsiz!\n\n🎉Siz barcha kanallarga obuna bo‘lgansiz!\n\n🎉 Film kodini yuborishingiz mumkin!")
        return

    buttons = []
    for channel in unsubscribed:
        if channel["type"] == "telegram":
            buttons.append([InlineKeyboardButton(text=channel["name"], url=f"https://t.me/{channel['username'].lstrip('@')}")])
        elif channel["type"] == "instagram":
            buttons.append([InlineKeyboardButton(text=channel["name"], url=channel["username"])])

    buttons.append([InlineKeyboardButton(text="Obunani tekshirish✅", callback_data="check_subscriptions")])

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    sent_msg = await message.answer("Iltimos, quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)
    last_messages[user_id] = sent_msg.message_id


@router.callback_query(lambda c: c.data == "check_subscriptions")
async def check_subscriptions(call: CallbackQuery):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    if user_id in last_messages:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=last_messages[user_id])
        except:
            pass

    unsubscribed = await check_user_subscriptions(bot, user_id)

    # Instagramni obuna bo'lgan deb hisoblaymiz
    instagram_subscribed = False
    if len(unsubscribed) < len([ch for ch in CHANNELS if ch['type'] == 'telegram']):
        instagram_subscribed = True  # Instagramga obuna bo'lgan deb hisoblash

    # Instagram sahifasini ro'yxatdan olib tashlash
    if instagram_subscribed:
        instagram_visited_users.add(user_id)
        unsubscribed = [channel for channel in unsubscribed if channel["type"] != "instagram"]

    if not unsubscribed:
        await call.message.answer("Botga xush kelibsiz!\n\n🎉Siz barcha kanallarga obuna bo‘lgansiz!\n\n🎉 Film kodini yuborishingiz mumkin!")
        await call.answer()
        return

    # Qolgan obuna bo'lmagan kanallarni ko'rsatish
    buttons = []
    for channel in unsubscribed:
        if channel["type"] == "telegram":
            buttons.append([InlineKeyboardButton(text=channel["name"], url=f"https://t.me/{channel['username'].lstrip('@')}")])

    buttons.append([InlineKeyboardButton(text="Obunani tekshirish✅", callback_data="check_subscriptions")])

    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    sent_msg = await call.message.answer("Hali obuna bo‘lmagan kanallaringiz:", reply_markup=markup)
    last_messages[user_id] = sent_msg.message_id

    await call.answer()
