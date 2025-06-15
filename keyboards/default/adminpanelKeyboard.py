from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_menu = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text="📊 Foydalanuvchilar soni"),
            KeyboardButton(text="📈 Foydalanuvchilar reytingi"),
        ],
        [
            KeyboardButton(text="🗞 Reklama yuborish"),
            KeyboardButton(text="📁 Yuklab olish"),
        ],
        [
            KeyboardButton(text="Konkursni qayta boshlash")
        ],
        [
            KeyboardButton(text="☎️ Dasturchi bilan bog'lanish")
        ]
    ],
    resize_keyboard=True
)
