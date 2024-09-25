from aiogram import Bot, Dispatcher, executor, types
import asyncio
import logging
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import pandas as pd
import matplotlib.pyplot as plt
import io

from keyboards import *
import texts


api = '7793599961:AAF9TpoAN_-gBdbV4q_-I02M0xU_FX8L2Ik'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f'✅ Добро пожаловать!\n\n' + texts.start, reply_markup=start_kb)


@dp.message_handler(Text(equals=['📋 Меню']))
async def send_menu(message: types.Message):
    # Отправляем список доступных команд
    await message.answer(
        "📋 Меню команд:\n"
        "/start - Перезапуск бота\n",
        reply_markup=start_kb
    )


@dp.message_handler(Text(equals=['ℹ️ О нас']))
async def send_info(message):
    await message.answer(texts.about_as, parse_mode='HTML', reply_markup=start_kb)


@dp.message_handler(Text(equals=['❓ Помощь']))
async def help_send(message):
    await message.answer('<b>Если есть вопросы</b>', parse_mode='HTML', reply_markup=buy_kb)


@dp.message_handler(Text(equals=['📊 Исследования']))
async def send_price_list(message):
    await message.answer('<b>Выберите интересующую вас услугу</b>', parse_mode='HTML', reply_markup=catalog_kb)


@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def handle_file(message: types.Message):
    # Проверяем, что файл - это CSV
    if message.document.mime_type == 'text/csv':
        # Скачиваем файл
        file_info = await bot.get_file(message.document.file_id)
        file_path = file_info.file_path
        file = await bot.download_file(file_path)

        # Чтение файла CSV в pandas
        data = pd.read_csv(file)

        # Предполагаем, что первая строка — это даты, остальные строки — числовые значения
        dates = data.columns.values[1:]  # Первый столбец пропускаем, если это не даты
        values = data.iloc[:, 1:].values  # Берем все строки, начиная со второго столбца

        # Строим график
        plt.figure(figsize=(10, 6))
        for i, row in enumerate(values):
            plt.plot(dates, row, label=f'Строка {i + 1}')

        plt.title('Визуализация данных из CSV')
        plt.xlabel('Даты')
        plt.ylabel('Значения')
        plt.grid(True)

        # Размещение легенды справа от графика
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # Легенда справа от графика

        # Сохраняем график в байтовый объект для отправки
        image_stream = io.BytesIO()
        plt.savefig(image_stream, format='png', bbox_inches='tight')  # Сохранение с учетом всех элементов
        image_stream.seek(0)  # Возвращаем курсор в начало файла

        # Отправляем изображение пользователю
        await message.answer_photo(photo=image_stream)

        # Закрываем график, чтобы очистить память
        plt.close()
    else:
        await message.reply("Пожалуйста, отправьте файл в формате CSV.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
