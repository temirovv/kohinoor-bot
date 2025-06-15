from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import db_admin


def make_channels_inline_for_admin():
    channels = db_admin.get_channels()
    menu = InlineKeyboardMarkup(row_width=2)
    buttons = []

    for channel in channels:
        channel_id, channel_name = channel
        buttons.append(
            InlineKeyboardButton(text=channel_name, callback_data=f"deleting.{channel_id}")
        )


    menu.row(*buttons)
    

    return menu
