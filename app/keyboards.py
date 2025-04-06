from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)

main_kb= ReplyKeyboardMarkup(
    keyboard= [
        [
        KeyboardButton(text="/admin")
        ]
    ],
    resize_keyboard= True,
    one_time_keyboard= True,
    input_field_placeholder= "Kodni kiriting !"
)

admin_kb= ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text="/reklama_yuborish"),
            KeyboardButton(text="/foydalanuvchilar_soni")
        ]
    ],
    resize_keyboard= True,
    one_time_keyboard= True,
    input_field_placeholder= "Admin paneli !"
)