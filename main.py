from aiogram import Bot, Dispatcher, executor, types
import asyncio
import logging
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
