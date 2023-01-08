import re

import pandas as pd
import requests

from typing import Optional


SPB_MEAN_CONSTRUCTION_YEAR = 2000
YEAR_TO_SUBTRACT_FROM = 2022


def get_search_string(address: str) -> str:
    """Преобразует адрес дома в поисковую строку для dom.mingkh.ru."""
    return '+'.join(address.strip().split())


def parse_houses_info(address: str) -> pd.DataFrame:
    """Возвращает характеристики дома по его адресу с сайта dom.mingkh.ru.

    В случае непустого ответа датафрейм будет содержать следующие колонки:
    Город,	Адрес,	Площадь м2,	 Год,  Этажей,	Жилых помещений.
    """
    search_string = get_search_string(address)

    results = pd.DataFrame()
    page_num = 1
    while True:
        response = requests.get(
            f'https://dom.mingkh.ru/search?address={search_string}&searchtype=house&page={page_num}'
        )
        list_of_tables = pd.read_html(response.content.decode())

        if list_of_tables[0].empty:
            break
        page_num += 1
        results = pd.concat([results, list_of_tables[0]])
    return results[results['Город'] == 'Санкт-Петербург'].copy()


def get_house_construction_year(df: pd.DataFrame, house_number: str) -> Optional[int]:
    """Возвращает год постройки дома.

    Если датафрейм пустой, то вернет значение SPB_MEAN_CONSTRUCTION_YEAR.
    В случае совпадения номера дома возвращает дату создания здания.
    Если дома с таким номером нет, то вернет средний возраст домов на этой улице.
    """
    if df.empty:
        return SPB_MEAN_CONSTRUCTION_YEAR
    # Выбрасываем записи с пропусками в году постройки
    df = df[~df['Год'].astype(str).str.contains('—')].copy()
    if df.empty:
        return SPB_MEAN_CONSTRUCTION_YEAR
    df['Год'] = df['Год'].astype(int)

    house_number_match = df['Адрес'].str.contains(rf'\s{house_number}\D', regex=True)
    if not any(house_number_match):
        # Если не нашли соответствие номера дома, то возвращаем средний год по улице
        return int(df['Год'].mean().round())
    # преобразование в int нужно для дальнейшей возможности отправки словаря в json'е request'а
    return int(df[house_number_match]['Год'].mean().round())


def estimate_house_age(address: str) -> int:
    """Оценивает возраст дома на основании данных dom.mingkh.ru."""
    houses_info = parse_houses_info(address)
    house_numbers = re.findall(r'\d+', address.split(', ')[-1])

    # Обработаем адреса типа 63-65, 35к1 -> для них вернется 63 и 35 соответственно
    # Для простых номеров типа 38, 34А -> для них вернется 38 и 34 соответственно
    house_number = house_numbers[-1]
    if len(house_numbers) > 1:
        house_number = house_numbers[0]
    return int(YEAR_TO_SUBTRACT_FROM - get_house_construction_year(houses_info, house_number))
