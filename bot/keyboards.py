from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from typing import List, Union


def get_reply_keyboard_markup(buttons_names: List[Union[str, int]]) -> ReplyKeyboardMarkup:
    keyboard = []
    row = []
    for idx, name in enumerate(buttons_names):
        row.append(KeyboardButton(name))
        if idx % 2 == 1:
            keyboard.append(row)
            row = []
            continue
        if idx + 1 == len(buttons_names):
            keyboard.append(row)
    keyboard.append(['/restart'])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
