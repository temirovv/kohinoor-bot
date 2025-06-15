from aiogram.dispatcher.filters.state import StatesGroup, State

class ControlChannel(StatesGroup):
    add_channel = State()
    delete_channel = State()
    add_admin = State()
