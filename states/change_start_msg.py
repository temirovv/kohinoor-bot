from aiogram.dispatcher.filters.state import StatesGroup, State

class ChangeStartMessage(StatesGroup):
    ch_msg = State()
    confirm_ch_msg = State()
