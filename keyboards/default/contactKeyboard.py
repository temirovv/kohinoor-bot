from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("📞 Raqamni yuborish", request_contact=True)]
    ],
    resize_keyboard=True,
)
