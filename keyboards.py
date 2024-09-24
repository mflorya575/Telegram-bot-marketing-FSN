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

catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text = 'Сайт 1', callback_data = 'Сайт 1'),
        ],
        [
            InlineKeyboardButton(text = 'Сайт 2', callback_data = 'Сайт 2'),
        ],
        [
            InlineKeyboardButton(text = 'Сайт 3', callback_data = 'Сайт 3'),
        ],
        [
            InlineKeyboardButton(text = 'Сайт 4', callback_data = 'Сайт 4'),
        ],
    ]
)


buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Написать", url = "https://t.me/jlosos1856"),
        ],
    ]
)
