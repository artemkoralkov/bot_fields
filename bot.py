import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from random import randint
import re
from db import (
    init_db,
    add_to_db,
    get_filed_names,
    get_field_numbers,
    get_messages,
)

# Инициализация базы данных
init_db()

# Вставьте сюда ваш токен API
API_TOKEN = 'YOUR_API_TOKEN'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

message_pattern = r"№\d+\w*\d*\s+[А-Я][а-я]+"

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я ваш бот. Используйте команду /view для просмотра сообщений или просто отправьте сообщение для добавления в базу.")

# Обработчик текстовых сообщений
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text_message(message: types.Message):
    message_text = message.text
    match = re.search(message_pattern, message_text)
    if match:
        part_to_remove = match.group(0)
        message_without_part = message_text.replace(part_to_remove, "").strip()
        field_number, field_name = part_to_remove.split()
        add_to_db(field_name, field_number, message_without_part)
        await message.reply("Сообщение добавлено.")
    else:
        await message.reply("Сообщение не соответствует требуемому формату.")

# Обработчик команды /view
@dp.message_handler(commands=['view'])
async def view_messages(message: types.Message):
    field_names = list(get_filed_names())
    if not field_names:
        await message.reply("Нет доступных полей.")
        return

    # Постраничная навигация
    page_size = 10  # Количество элементов на странице
    pages = [field_names[i:i + page_size] for i in range(0, len(field_names), page_size)]
    current_page = 0

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for name in pages[current_page]:
        keyboard.add(name)

    # Добавляем кнопки для навигации
    if len(pages) > 1:
        if current_page > 0:
            keyboard.add("⬅️ Предыдущая")
        if current_page < len(pages) - 1:
            keyboard.add("Следующая ➡️")

    await message.reply("Выберите поле:", reply_markup=keyboard)
    await dp.current_state(user=message.from_user.id).set_state("waiting_for_field_name")
    await dp.current_state(user=message.from_user.id).update_data(pages=pages, current_page=current_page)

@dp.message_handler(state="waiting_for_field_name")
async def process_field_name_step(message: types.Message, state):
    data = await state.get_data()
    pages = data.get("pages")
    current_page = data.get("current_page")

    if message.text == "⬅️ Предыдущая":
        current_page -= 1
    elif message.text == "Следующая ➡️":
        current_page += 1
    else:
        selected_field_name = message.text
        field_numbers = list(get_field_numbers(selected_field_name))
        if not field_numbers:
            await message.reply("Нет доступных номеров для выбранного поля.")
            return

        # Постраничная навигация для номеров
        page_size = 10
        number_pages = [field_numbers[i:i + page_size] for i in range(0, len(field_numbers), page_size)]
        current_number_page = 0

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for number in number_pages[current_number_page]:
            keyboard.add(number)

        if len(number_pages) > 1:
            if current_number_page > 0:
                keyboard.add("⬅️ Предыдущая")
            if current_number_page < len(number_pages) - 1:
                keyboard.add("Следующая ➡️")

        await message.reply("Выберите номер:", reply_markup=keyboard)
        await dp.current_state(user=message.from_user.id).set_state("waiting_for_field_number")
        await state.update_data(selected_field_name=selected_field_name, number_pages=number_pages, current_number_page=current_number_page)
        return

    keyboard =
