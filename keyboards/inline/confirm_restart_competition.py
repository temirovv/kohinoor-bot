from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


cofirm_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton("Ha tasdiqlayman", callback_data="yes_i_confirm"),
            InlineKeyboardButton("Yo'q rad etaman", callback_data="no_i_reject")
        ]
    ]
)
