from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

for_users = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📊 Reyting"),
            KeyboardButton(text="💫 Jami ball"),
            KeyboardButton(text="Do'stlarni taklif qilish")
        ],
        [
            KeyboardButton(text="📞 Biz bilan aloqa")
        ],
        [
            KeyboardButton(text="🗂 Mening ma‘lumotlarim")
        ]
    ],
    resize_keyboard=True
)
