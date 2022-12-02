from aiogram import Bot, Dispatcher, executor, types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN_API

bot = Bot(token=TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

price = '<b>Этот текст представляет собой цену. Скоро ее будет генерировать ML-модель</b>'

welcome_text = """
Бот разработан для предсказания цены недвижимости в Санкт-Петербурге
Работать с ботом очень просто.
Вы постепенно вводите параметры своей квартиры, а бот предсказывает ее цену на каждом шаге.
"""

start_work_text = """
На каждом шаге будет предложено ввести значение для параметра. \n
Чем больше параметров введете - тем точнее предсказанная цена.
Если не знаете или не хотите вводить значение параметра,
напишите <b>Пропустить этот параметр</b>, либо используйте соответствующую кнопку"""

github_link = 'https://github.com/NeKonnnn/PetProject-price-real-estate-in-St.-Petersburg'


class ClientStatesGroup(StatesGroup):
    number_of_rooms = State()
    total_area = State()
    living_area = State()
    floor = State()
    location = State()


class Feedback(StatesGroup):
    feedback = State()


start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add(KeyboardButton('Начать работу'))
start_keyboard.add(KeyboardButton('Репозиторий GitHub'))
start_keyboard.add(KeyboardButton('Написать авторам'))

keyboard_during_work = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_during_work.add(KeyboardButton('Пропустить этот параметр'))
keyboard_during_work.add(KeyboardButton('Вернуться в главное меню'))


@dp.message_handler(commands=['start'], state='*')
async def command_start(message: types.Message, state: FSMContext):
    await message.answer(text=welcome_text,
                         reply_markup=start_keyboard)
    await state.finish()


@dp.message_handler(Text(equals='Вернуться в главное меню'), state='*')
async def go_to_main_menu(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply(text='Открыто главное меню',
                        reply_markup=start_keyboard)
    await state.finish()


@dp.message_handler(Text(equals='Начать работу', ignore_case=True), state=None)
async def start_work(message: types.Message) -> None:
    await ClientStatesGroup.number_of_rooms.set()
    await message.answer(text=start_work_text, parse_mode='HTML')
    await message.answer("""Шаг 1️⃣. Введите число комнат""", reply_markup=keyboard_during_work)


@dp.message_handler(Text(equals='Репозиторий GitHub'))
async def get_github(message: types.Message) -> None:
    await message.answer(text=github_link)


@dp.message_handler(Text(equals='Написать авторам'))
async def get_feedback(message: types.Message) -> None:
    await message.answer('Напишите отзыв/пожелание/замечание и я отправлю его авторам')
    await Feedback.feedback.set()


@dp.message_handler(state=ClientStatesGroup.number_of_rooms)
async def feature1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text != 'Пропустить этот параметр':
            data['number_of_rooms'] = message.text
            await message.answer(f'При данных параметрах оцениваем квартиру в стоимость {price} рублей', parse_mode='HTML')
        else:
            data['number_of_rooms'] = None
    await ClientStatesGroup.next()
    await message.answer(text="""Шаг 2️⃣. Введите общую площадь""", reply_markup=keyboard_during_work)


@dp.message_handler(state=ClientStatesGroup.total_area)
async def feature2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text != 'Пропустить этот параметр':
            data['total_area'] = message.text
            await message.answer(f'При данных параметрах оцениваем квартиру в стоимость {price} рублей', parse_mode='HTML')
        else:
            data['total_area'] = None

    await ClientStatesGroup.next()
    await message.answer(text="""Шаг 3️⃣. Введите жилую площадь""", reply_markup=keyboard_during_work)


@dp.message_handler(state=ClientStatesGroup.living_area)
async def feature3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text != 'Пропустить этот параметр':
            data['living_area'] = message.text
            await message.answer(f'При данных параметрах оцениваем квартиру в стоимость {price} рублей', parse_mode='HTML')
        else:
            data['living_area'] = None
    await ClientStatesGroup.next()
    await message.answer(text="""Шаг 4️⃣. Введите этаж""", reply_markup=keyboard_during_work)


@dp.message_handler(state=ClientStatesGroup.floor)
async def feature4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text != 'Пропустить этот параметр':
            data['floor'] = message.text
            await message.answer(f'При данных параметрах оцениваем квартиру в стоимость {price} рублей', parse_mode='HTML')
        else:
            data['floor'] = None
    await ClientStatesGroup.next()
    await message.answer(text="""Шаг 5️⃣. Введите адрес""", reply_markup=keyboard_during_work)


@dp.message_handler(state=ClientStatesGroup.location)
async def feature5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text != 'Пропустить этот параметр':
            data['location'] = message.text
        else:
            data['location'] = None

    async with state.proxy() as data:
        await message.answer(f"""
Параметры сохранены \n
Вы ввели параметры:
Количество комнат - {data['number_of_rooms']}
Общая площадь - {data['total_area']}
Жилая площадь - {data['living_area']}
Этаж - {data['floor']}
Адрес - {data['location']}

При заданных параметрах квартира оценивается в {price} рублей""", parse_mode='HTML', reply_markup=start_keyboard)
    await state.finish()


@dp.message_handler(state=Feedback.feedback)
async def send_feedback(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['feedback'] = message.text
        await message.answer('Спасибо! Ваше сообщение отправлено')
        await bot.send_message(chat_id='766828537', text=f"Пришло сообщение от пользователя {message.from_user.id}: {data['feedback']}")
        await state.finish()


async def on_startup(_):
    print('Бот запущен. Этот текст выводится в консоль')


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)
