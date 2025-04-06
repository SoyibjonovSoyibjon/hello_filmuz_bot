from aiogram import F
from aiogram.types import Message
from app import keyboards as kb
from main import bot
from handlers import router, botAdmin

def is_admin(user_id: int) -> bool:
    return user_id in botAdmin

@router.message(F.text == '/admin_paneli')
async def cmd_admin_paneli(message: Message):
    # chat_member= await bot.get_chat_member(chat_id=message.chat.id, user_id= message.from_user.id)

    if message.from_user.id not in botAdmin:
        await message.answer("Kechirasiz ushbu buyruq faqat adminlar uchun !")
        return
    await message.answer("<strong>Admin paneliga o‘tdingiz !</strong>",reply_markup=kb.admin_kb , parse_mode='HTML')

@router.message(F.text == '/reklama_yuborish')
async def cmd_reklama_yuborish(message: Message):
    if is_admin(message.from_user.id):
        await message.answer('Reklama yuborish !')
        return
    
@router.message(F.text == '/foydalanuvchilar_soni')
async def cmd_reklama_yuborish(message: Message):
    if is_admin(message.from_user.id):
        await message.answer('Foydalanuvchilar sonini ko‘rish !')
        return