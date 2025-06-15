from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def make_inline_kb(text='', url=None, call_backdata=None):
    
    button = InlineKeyboardButton(
        text=text,
        url= url,
        callback_data=call_backdata
    )
    
    return button
