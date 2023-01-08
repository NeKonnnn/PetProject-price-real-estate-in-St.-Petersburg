from typing import Tuple

import requests

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from json import JSONDecodeError

from address_converter import get_address_data, YandexAPIRespondStatus
from metro_features_calculation import calculate_metro_distances
from house_age_parser import estimate_house_age
from client_states import ClientStates
from config import TOKEN_API, ML_APP_URL
from keyboards import get_reply_keyboard_markup
from messages_for_menus import (
    text_output_for_command,
    HELP_INFO,
    service_not_available_respond_text,
    format_model_response,
    format_user_features,
)

bot = Bot(token=TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


def convert_text_to_float(text: str, left_num: int = 1, right_num: int = 500) -> Tuple[float, bool]:
    """Преобразует строку в число и проверяет лежит ли оно между left_num и right_num."""
    try:
        number = float(text.replace(',', '.'))
        return number, left_num < number <= right_num
    except ValueError:
        return 0, False


@dp.message_handler(commands=['start', 'restart'], state='*')
async def start_message(message: types.Message):
    await bot.send_message(
        text=HELP_INFO,
        chat_id=message.from_user.id,
        reply_markup=get_reply_keyboard_markup(['/estimate', '/help', '/repository', '/about']),
        parse_mode='HTML',
    )
    await message.delete()
    await ClientStates.main_menu.set()


@dp.message_handler(commands=list(text_output_for_command.keys()), state=ClientStates.main_menu)
async def html_out_command(message: types.Message):
    """Выводит информацию в виде HTML."""
    await bot.send_message(
        text=text_output_for_command[message.text[1:]],
        chat_id=message.from_user.id,
        parse_mode='HTML',
    )
    await message.delete()


@dp.message_handler(commands=['estimate'], state=ClientStates.main_menu)
async def estimate_command(message: types.Message):
    await ClientStates.address.set()
    await bot.send_message(
        text='Шаг 1️⃣. Введите адрес интересующего вас дома, например: ул. Пушкина, 9.',
        chat_id=message.from_user.id,
        reply_markup=get_reply_keyboard_markup([])
    )
    await message.delete()


@dp.message_handler(state=ClientStates.address)
async def parse_address(message: types.Message, state: FSMContext):
    respond = get_address_data(message.text)
    if respond.status == YandexAPIRespondStatus.service_not_available:
        await ClientStates.main_menu.set()
        await bot.send_message(
            text=service_not_available_respond_text,
            chat_id=message.from_user.id,
            reply_markup=get_reply_keyboard_markup(['/estimate', '/help', '/help', '/about'])
        )
        return

    if respond.status == YandexAPIRespondStatus.multiple_found:
        await bot.send_message(
            text='По вашему адресу найдено несколько домов. Уточните, пожалуйста, адрес.',
            chat_id=message.from_user.id,
            reply_markup=get_reply_keyboard_markup([])
        )
        return

    if respond.status == YandexAPIRespondStatus.nothing_found:
        await bot.send_message(
            text='По вашему адресу дом не найден. Уточните, пожалуйста, адрес.',
            chat_id=message.from_user.id,
            reply_markup=get_reply_keyboard_markup([])
        )
        return

    await ClientStates.number_of_rooms.set()
    await bot.send_message(
        text=f'По указанному вами адресу найден дом. Полный адрес: {respond.formatted_address}',
        chat_id=message.from_user.id,
        reply_markup=get_reply_keyboard_markup([])
    )
    async with state.proxy() as data:
        data['address'] = respond.formatted_address
        data['latitude'] = respond.latitude
        data['longitude'] = respond.longitude
        data['building_age'] = estimate_house_age(respond.formatted_address)
        data.update(
            calculate_metro_distances(house_latitude=respond.latitude, house_longitude=respond.longitude)
        )
    await bot.send_message(
        text="""Шаг 2️⃣. Введите число комнат""",
        chat_id=message.from_user.id,
        reply_markup=get_reply_keyboard_markup(['0 (студия)', 1, 2, 3, 4, 5, 6])
    )
    await message.delete()


@dp.message_handler(
    lambda message: (message.text.isdigit() and 0 <= int(message.text) < 7) or message.text == '0 (студия)',
    state=ClientStates.number_of_rooms
)
async def get_number_of_rooms(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['rooms'] = int(message.text) if message.text.isdigit() else 0
    await bot.send_message(
        text="""Шаг 3️⃣. Введите площадь квартиры""",
        chat_id=message.from_user.id,
        reply_markup=get_reply_keyboard_markup([])
    )
    await ClientStates.next()


@dp.message_handler(state=ClientStates.number_of_rooms)
async def retry_number_of_rooms(message: types.Message):
    await bot.send_message(
        text='Неверный формат числа! Введите количество комнат в квартире (целое число от 1 до 6)',
        chat_id=message.from_user.id,
        reply_markup=get_reply_keyboard_markup(['0 (студия)', 1, 2, 3, 4, 5, 6]),
    )


@dp.message_handler(
    lambda message: convert_text_to_float(message.text)[1],
    state=ClientStates.total_area
)
async def get_total_area(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['total_area'] = convert_text_to_float(message.text)[0]
    await bot.send_message(
        text="""Шаг 3️⃣. Введите этаж, на котором находится квартира.""",
        chat_id=message.from_user.id,
        reply_markup=get_reply_keyboard_markup([])
    )
    await ClientStates.next()


@dp.message_handler(state=ClientStates.total_area)
async def retry_total_area(message: types.Message):
    await bot.send_message(
        text='Неверный формат числа! Введите количество кв.м. в квартире (от 1 до 500)',
        chat_id=message.from_user.id,
        reply_markup=get_reply_keyboard_markup([]),
    )


@dp.message_handler(
    lambda message: message.text.isdigit() and 0 < int(message.text) <= 50,
    state=ClientStates.stage
)
async def get_floor(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['stage'] = int(message.text)
    await bot.send_message(
        text="""Шаг 4️⃣. В квартире есть балкон/лоджия?""",
        chat_id=message.from_user.id,
        reply_markup=get_reply_keyboard_markup(['да', 'нет'])
    )
    await ClientStates.next()


@dp.message_handler(state=ClientStates.stage)
async def retry_floor(message: types.Message):
    await bot.send_message(
        text='Неверный формат числа! Введите этаж квартиры (целое число от 1 до 50)',
        chat_id=message.from_user.id,
        reply_markup=get_reply_keyboard_markup([]),
    )


@dp.message_handler(regexp='|'.join(['да', 'нет']), state=ClientStates.balcony)
async def get_balcony(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['balcony'] = 1 if message.text == 'да' else 0
    await bot.send_message(
        text="""Шаг 5️⃣. Есть ли лифт в подъезде?""",
        chat_id=message.from_user.id,
        reply_markup=get_reply_keyboard_markup(['да', 'нет'])
    )
    await ClientStates.next()


@dp.message_handler(state=ClientStates.balcony)
async def retry_balcony(message: types.Message):
    await bot.send_message(
        text='Неверный вариант ответа. Есть ли балкон/лоджия в квартире (ответьте да или нет)?',
        chat_id=message.from_user.id,
        reply_markup=get_reply_keyboard_markup(['да', 'нет']),
    )


@dp.message_handler(regexp='|'.join(['да', 'нет']), state=ClientStates.elevator)
async def get_elevator(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'нет':
            data['elevator'] = 0
            data['largage_elevator'] = 0
            await ClientStates.model_response.set()
            await bot.send_message(
                text="""Хотите ли получить примерную стоимость квартиры?""",
                chat_id=message.from_user.id,
                reply_markup=get_reply_keyboard_markup(['Рассчитать стоимость!'])
            )
            return
        data['elevator'] = 1

    await bot.send_message(
        text="""Заключительный вопрос! Есть ли грузовой лифт в подъезде?""",
        chat_id=message.from_user.id,
        reply_markup=get_reply_keyboard_markup(['да', 'нет'])
    )
    await ClientStates.next()


@dp.message_handler(state=ClientStates.elevator)
async def retry_elevator(message: types.Message):
    await bot.send_message(
        text='Неверный вариант ответа. Есть ли лифт в подъезде (ответьте да или нет)?',
        chat_id=message.from_user.id,
        reply_markup=get_reply_keyboard_markup(['да', 'нет']),
    )


@dp.message_handler(regexp='|'.join(['да', 'нет']), state=ClientStates.largage_elevator)
async def get_largage_elevator(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['largage_elevator'] = 1 if message.text == 'да' else 0

    await bot.send_message(
        text="""Хотите ли рассчитать примерную стоимость квартиры?""",
        chat_id=message.from_user.id,
        reply_markup=get_reply_keyboard_markup(['Рассчитать стоимость!'])
    )
    await ClientStates.next()


@dp.message_handler(state=ClientStates.largage_elevator)
async def retry_largage_elevator(message: types.Message):
    await bot.send_message(
        text='Неверный вариант ответа. Есть ли грузовой лифт в подъезде (ответьте да или нет)?',
        chat_id=message.from_user.id,
        reply_markup=get_reply_keyboard_markup(['да', 'нет']),
    )


@dp.message_handler(Text(equals=['Рассчитать стоимость!', 'Да', 'да']), state=ClientStates.model_response)
async def get_model_response(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        features_repr = format_user_features(data)
        print(data.as_dict())
        try:
            features = {key: value for key, value in data.as_dict().items() if key != 'address'}
            prices = requests.post(url=ML_APP_URL, json=features).json()
        except JSONDecodeError:
            await bot.send_message(
                text=service_not_available_respond_text,
                chat_id=message.from_user.id,
                reply_markup=get_reply_keyboard_markup([])
            )
            return
    features_repr += format_model_response(prices)
    await bot.send_message(
        text=features_repr,
        chat_id=message.from_user.id,
        parse_mode='HTML',
        reply_markup=get_reply_keyboard_markup(['/estimate', '/help', '/repository', '/about']),
    )
    await ClientStates.main_menu.set()


@dp.message_handler(state=ClientStates.model_response)
async def retry_model_response(message: types.Message):
    await bot.send_message(
        text='Может все-таки посмотрите цену? Не зря же вы все это время потратили?)',
        chat_id=message.from_user.id,
        reply_markup=get_reply_keyboard_markup(['Рассчитать стоимость!']),
    )


async def on_startup(_):
    print('Бот запущен.')


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
