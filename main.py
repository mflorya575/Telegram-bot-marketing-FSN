import aiohttp
from aiogram import Bot, Dispatcher, executor, types
import asyncio
import logging
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import pandas as pd
import matplotlib.pyplot as plt
import io
import requests as requests
from bs4 import BeautifulSoup

from keyboards import *
import texts


api = '7793599961:AAF9TpoAN_-gBdbV4q_-I02M0xU_FX8L2Ik'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Список для хранения ссылок на статьи
article_links = []

# URL сайта для парсинга
URL = "https://www.sostav.ru/news/marketing"


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f'✅ Добро пожаловать!\n\n' + texts.start, reply_markup=start_kb)


@dp.message_handler(Text(equals=['📋 Меню']))
async def send_menu(message: types.Message):
    # Отправляем список доступных команд
    await message.answer(
        "📋 <b>Команды бота:</b>\n"
        "/start - Перезапуск бота.\n"
        "/parse - Парсинг статей с сайта маркетинговых исследований. Затем можно нажимать на кнопку Исследования.\n"
        "/help - Показать это сообщение с доступными командами.\n",
        reply_markup=start_kb, parse_mode='HTML'
    )


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    help_text = (
        "<b>Команды бота:</b>\n\n"
        "/start - Перезапуск бота.\n"
        "/parse - Парсинг статей с сайта маркетинговых исследований. Затем можно нажимать на кнопку Исследования.\n"
        "/help - Показать это сообщение с доступными командами.\n"
    )
    await message.answer(help_text, parse_mode='HTML')


@dp.message_handler(Text(equals=['ℹ️ О нас']))
async def send_info(message):
    await message.answer(texts.about_as, parse_mode='HTML', reply_markup=start_kb)


@dp.message_handler(Text(equals=['❓ Помощь']))
async def help_send(message):
    await message.answer('<b>Если есть вопросы</b>', parse_mode='HTML', reply_markup=buy_kb)

# ----------------------------------------------------


@dp.message_handler(commands=['parse'])
async def manual_parse(message: types.Message):
    await parse_new_articles()
    await message.reply("Парсинг завершён.")


# Асинхронная функция для парсинга сайта и получения новых статей
async def parse_new_articles():
    global article_links
    logging.info("Начинаем парсинг сайта...")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(URL) as response:
                logging.info(f"Статус ответа: {response.status}")
                if response.status == 200:
                    html = await response.text()

                    # Вывод первых 500 символов страницы для проверки
                    logging.info("HTML содержимое страницы: %s", html[:500])

                    soup = BeautifulSoup(html, "html.parser")

                    # Поиск статей с проверкой селектора
                    articles = soup.find_all('a', class_='title')
                    logging.info(f"Найдено статей: {len(articles)}")

                    # Печатаем заголовки для проверки
                    logging.info("Заголовки статей:")
                    for article in articles:
                        logging.info(article.get_text(strip=True))

                    # Очищаем старые ссылки и обновляем их новыми
                    article_links = []
                    for article in articles[:10]:  # Возьмем первые 10 статей
                        title = article.get_text(strip=True)  # Получаем заголовок статьи, очищая лишние пробелы
                        # Проверяем, начинается ли ссылка с 'http'
                        link = article['href'] if article['href'].startswith('http') else URL + article['href']

                        # Заменяем 'news/marketing' на 'publication/' в ссылке
                        if 'news/marketing' in link:
                            link = link.replace('news/marketing', '')

                        article_links.append((title, link))  # Добавляем заголовок и ссылку в список
                        logging.info(f"Добавлена статья: {title} - {link}")
                else:
                    logging.error(f"Ошибка запроса: {response.status}")
        except Exception as e:
            logging.error(f"Ошибка при парсинге: {e}")


# Функция для создания клавиатуры с новыми ссылками
def get_catalog_keyboard():
    catalog_kb = InlineKeyboardMarkup()
    for title, link in article_links:
        catalog_kb.add(InlineKeyboardButton(text=title, url=link))
    return catalog_kb


# Хэндлер, который отвечает за вывод кнопок
@dp.message_handler(Text(equals=['📊 Исследования']))
async def send_price_list(message: types.Message):
    if not article_links:
        await message.answer('Ссылки на статьи пока недоступны. Попробуйте позже.')
    else:
        await message.answer('<b>Выберите интересующую вас статью</b>', parse_mode='HTML',
                             reply_markup=get_catalog_keyboard())


# Запуск парсера с периодичностью в 1 час
async def on_startup(dp):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(parse_new_articles, 'interval', hours=1)  # Парсим сайт раз в час
    scheduler.start()

#------------------------------------------------------


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

        # Отправляем три отдельных графика

        # Первый график: линейная диаграмма
        fig, ax = plt.subplots(figsize=(10, 6))
        for i, row in enumerate(values):
            ax.plot(dates, row, label=f'Строка {i + 1}')

        ax.set_title('Линейная визуализация данных из CSV')
        ax.set_xlabel('Даты')
        ax.set_ylabel('Значения')
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # Легенда справа от графика
        ax.grid(True)

        # Сохраняем первый график в байтовый объект
        line_chart_stream = io.BytesIO()
        plt.savefig(line_chart_stream, format='png', bbox_inches='tight')
        line_chart_stream.seek(0)

        # Отправляем первый график пользователю
        await message.answer_photo(photo=line_chart_stream)

        # Закрываем первый график
        plt.close(fig)

        # Второй график: столбчатая диаграмма (Bar Chart)
        fig, ax = plt.subplots(figsize=(10, 6))
        summed_values = data.iloc[:, 1:].sum()  # Суммируем значения по строкам
        ax.bar(dates, summed_values)
        ax.set_title('Столбчатая диаграмма суммарных значений по датам')
        ax.set_xlabel('Даты')
        ax.set_ylabel('Сумма значений')

        # Сохраняем второй график в байтовый объект
        bar_chart_stream = io.BytesIO()
        plt.savefig(bar_chart_stream, format='png', bbox_inches='tight')
        bar_chart_stream.seek(0)

        # Отправляем второй график пользователю
        await message.answer_photo(photo=bar_chart_stream)

        # Закрываем второй график
        plt.close(fig)

        # Третий график: круговая диаграмма (Pie Chart)
        fig, ax = plt.subplots(figsize=(10, 6))
        total_values = summed_values  # Используем суммы значений для круговой диаграммы
        ax.pie(total_values, labels=dates, autopct='%1.1f%%', startangle=90)
        ax.set_title('Круговая диаграмма распределения значений по датам')

        # Сохраняем третий график в байтовый объект
        pie_chart_stream = io.BytesIO()
        plt.savefig(pie_chart_stream, format='png', bbox_inches='tight')
        pie_chart_stream.seek(0)

        # Отправляем третий график пользователю
        await message.answer_photo(photo=pie_chart_stream)

        # Закрываем третий график
        plt.close(fig)
    else:
        await message.reply("Пожалуйста, отправьте файл в формате CSV.")


@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def handle_excel_file(message: types.Message):
    # Проверяем, что файл - это Excel
    if message.document.mime_type in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                        'application/vnd.ms-excel']:
        # Скачиваем файл
        file_info = await bot.get_file(message.document.file_id)
        file_path = file_info.file_path
        file = await bot.download_file(file_path)

        # Чтение файла Excel в pandas
        data = pd.read_excel(file)

        # Предполагаем, что первая строка — это даты, остальные строки — числовые значения
        dates = data.columns.values  # Все столбцы (даты)
        values = data.values[1:]  # Все строки, начиная со второго

        # Создаем фигуру для дашборда с тремя графиками
        fig, axs = plt.subplots(3, 1, figsize=(10, 18))

        # Первый график: линейная диаграмма
        for i, row in enumerate(values):
            axs[0].plot(dates, row, label=f'Строка {i + 1}')

        axs[0].set_title('Линейная визуализация данных из Excel')
        axs[0].set_xlabel('Даты')
        axs[0].set_ylabel('Значения')
        axs[0].legend(loc='center left', bbox_to_anchor=(1, 0.5))  # Легенда справа от графика
        axs[0].grid(True)

        # Второй график: столбчатая диаграмма (Bar Chart)
        summed_values = data.iloc[1:].sum()  # Суммируем значения по строкам
        axs[1].bar(dates[1:], summed_values)  # Используем dates[1:], чтобы пропустить первый заголовок
        axs[1].set_title('Столбчатая диаграмма суммарных значений по датам')
        axs[1].set_xlabel('Даты')
        axs[1].set_ylabel('Сумма значений')

        # Третий график: круговая диаграмма (Pie Chart)
        total_values = summed_values  # Используем суммы значений для круговой диаграммы
        axs[2].pie(total_values, labels=dates[1:], autopct='%1.1f%%', startangle=90)
        axs[2].set_title('Круговая диаграмма распределения значений по датам')

        # Сохраняем дашборд в байтовый объект для отправки
        dashboard_stream = io.BytesIO()
        plt.tight_layout()  # Для корректного отображения элементов
        plt.savefig(dashboard_stream, format='png', bbox_inches='tight')
        dashboard_stream.seek(0)

        # Отправляем дашборд пользователю
        await message.answer_photo(photo=dashboard_stream)

        # Закрываем график, чтобы очистить память
        plt.close(fig)
    else:
        await message.reply("Пожалуйста, отправьте файл в формате Excel (.xlsx).")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
