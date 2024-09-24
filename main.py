from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio


api = '7793599961:AAF9TpoAN_-gBdbV4q_-I02M0xU_FX8L2Ik'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(text=['Хай', 'Programming'])
async def all_message(message: types.Message):
    await message.answer('Привет, друг!')


@dp.message_handler(commands=['example'])
async def command_example(message: types.Message):
    await message.answer('Была отправлена команда /example')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)
