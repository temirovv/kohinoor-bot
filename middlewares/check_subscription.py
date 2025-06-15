import logging
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


from utils.misc import subscription
from loader import bot, db, db_admin
from keyboards.inline.channels_keyboard import check_sub


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):    
        menu = InlineKeyboardMarkup() 
        CHANNEL = db_admin.get_channels_as_a_list()
        print(CHANNEL)
        if update.message:
            if update.message.chat.type != types.ChatType.PRIVATE:
                return types.ChatType.is_private

            telegram_id = update.message.from_user.id
            checking_invitation = update.message.get_args()
            user = update.message.from_user.id
            if update.message.text in ['/start', '/help']:
                return
            elif checking_invitation:
                return
        elif update.callback_query:
            if update.callback_query.message.chat.type != types.ChatType.PRIVATE:
                return types.ChatType.is_private
            
            user = update.callback_query.from_user.id
            if update.callback_query.data == "check_subs":
                return
        else:
            return

        result = "❗️Botdan toʻliq foydalanish uchun bizning Telegram sahifalarimizga obuna boʻling:\n"
        print('tekshirildi')
        final_status = True
        for channel in CHANNEL:
            status = await subscription.check(user_id=user,
                                              channel=channel)
            final_status *= status
            channel = await bot.get_chat(channel)
            if not status:
                invite_link = await channel.export_invite_link()
                button = InlineKeyboardButton(
                    text=channel.title,
                    url=invite_link
                )
                menu.add(button)
                result += (f"👉 <a href='{invite_link}'>{channel.title}</a>\n")

        if not final_status:
            menu.add(check_sub)
            await update.message.answer(result, disable_web_page_preview=True, reply_markup=menu)
            menu.inline_keyboard = []
            raise CancelHandler()
