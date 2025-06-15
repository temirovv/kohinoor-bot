from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

check_subs = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("Tekshirish ✅", callback_data="check_subs")
        ],
    ]
)
