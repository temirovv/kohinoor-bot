import logging

from aiogram import Dispatcher

from utils.db_api.db_admin import Admin

db_admin1 = Admin(path_to_db='data/admin.sqlite3')


async def on_startup_notify(dp: Dispatcher):
    ADMINS = db_admin1.get_adminstrators_as_list()

    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Bot ishga tushdi")

        except Exception as err:
            logging.exception(err)
