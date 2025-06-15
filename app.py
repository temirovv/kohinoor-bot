from aiogram import executor

from loader import dp, db, db_admin
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    db.create_table_users()
    db.create_table_admins()
    db.create_table_channels()
    db.create_table_groups()
    db_admin.create_table_messages_for_start()
    db_admin.create_table_konkurs()
    db_admin.create_channel_table()
    db_admin.create_adminstrator_table()
    # db_admin.set_konkurs1()
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
