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
            InlineKeyboardButton(text='Сайт 1', callback_data='Сайт 1', url='https://www.sostav.ru/publication/otpusk-70291.html'),
        ],
        [
            InlineKeyboardButton(text='Сайт 2', callback_data='Сайт 2', url='https://www.sostav.ru/publication/predvzyatoe-otnoshenie-v-trudovoj-sfere-70277.html'),
        ],
        [
            InlineKeyboardButton(text='Сайт 3', callback_data='Сайт 3', url='https://www.sostav.ru/publication/reklamnye-kompanii-trebuyut-s-distribyutorov-avto-1-mlrd-rublej-70271.html'),
        ],
        [
            InlineKeyboardButton(text='Сайт 4', callback_data='Сайт 4', url='https://www.sostav.ru/publication/zadajte-vopros-direktoru-departamenta-marketingovykh-kommunikatsij-mts-marii-yakovlevoj-70259.html'),
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
