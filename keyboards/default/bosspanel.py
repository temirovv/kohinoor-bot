from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

boss_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="gruppa qo'shish", callback_data="add_group"),
            InlineKeyboardButton(text="kanal qo'shish", callback_data="add_channel"),
        ],
        [
            InlineKeyboardButton(text="admin tayinlash", callback_data="add_admin")
        ]
    ]
)


