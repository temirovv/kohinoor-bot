from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ch_start_msg = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ha", callback_data="confirm_changing_start_message"),
            InlineKeyboardButton(text="Yo'q", callback_data="deny_changing_start_message")
        ]
    ]
)
