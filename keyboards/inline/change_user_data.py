from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


change_user_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Bekor qilish", callback_data="deny_changing_user_name")
        ]
    ]
)

confirm_changing = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ha", callback_data="confirm_changing_operate")
        ],
        [
            InlineKeyboardButton(text="Yo'q", callback_data="deny_changing_operate")
        ]
    ]
)
