from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='❓ Помощь'),
            KeyboardButton(text='ℹ️ О нас'),
            KeyboardButton(text='📊 Исследования')
        ],
        [
            KeyboardButton(text='📋 Меню')  # Кнопка для вызова меню
        ],
    ], resize_keyboard=True
)

buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Написать", url="https://t.me/durov"),
        ],
    ]
)
