from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


confirm_ad_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ha", callback_data="yes_i_confirm_advert"),
            InlineKeyboardButton(text="Yo'q", callback_data="no_i_reject_advert")
        ]
    ]    
)