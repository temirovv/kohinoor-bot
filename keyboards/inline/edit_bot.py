from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


edit_bot_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="start tugmasini bosganda", callback_data="edit_start_message"),
            # InlineKeyboardButton(text="")

        ]
    ]
)
