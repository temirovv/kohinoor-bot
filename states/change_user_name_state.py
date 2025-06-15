from aiogram.dispatcher.filters.state import StatesGroup, State

class ChangeFullName(StatesGroup):
    change_full_name = State()
    confirm_changin_name = State()
    reject_changin_name = State()
