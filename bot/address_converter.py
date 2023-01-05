from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

import requests


class YandexAPIRespondStatus(Enum):
    nothing_found = 0
    match_found = 1
    multiple_found = 2
    service_not_available = 404


@dataclass
class YandexAPIData:
    status: YandexAPIRespondStatus
    latitude: float = 0
    longitude: float = 0
    formatted_address: str = ''


def append_city_name(address: str, city_name: str = 'Санкт-Петербург'):
    """Добавляет в начало адреса название города."""
    return f'{city_name}, {address}'


def parse_respond(api_respond: Optional[Dict[str, Any]]) -> YandexAPIData:
    """Дешифрует ответ API geocode-maps.yandex.ru."""
    if not api_respond:
        return YandexAPIData(status=YandexAPIRespondStatus.service_not_available)

    geo_object_collection = api_respond.get('response')['GeoObjectCollection']
    n_addresses_found = int(
        geo_object_collection['metaDataProperty']['GeocoderResponseMetaData']['found']
    )
    if n_addresses_found == 0:
        return YandexAPIData(status=YandexAPIRespondStatus.nothing_found)

    geo_objects = geo_object_collection['featureMember']
    matches = [
        geo_object for geo_object in geo_objects
        # Можем получить соответствие, но это может быть обобщение до координат города, а не дома.
        if geo_object['GeoObject']['metaDataProperty']['GeocoderMetaData']['precision'] == 'exact'
    ]

    if not matches:
        return YandexAPIData(status=YandexAPIRespondStatus.nothing_found)

    coordinates = matches[0]['GeoObject']['Point']['pos'].split()
    formatted_address = matches[0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
    return YandexAPIData(
        status=YandexAPIRespondStatus.match_found,
        formatted_address=formatted_address,
        latitude=float(max(coordinates)),
        longitude=float(min(coordinates)),
    )


def get_address_data(address: str) -> YandexAPIData:
    """Возвращает YandexAPIData, содержащий данные о доме по переданному адресу.

    В полученных данных содержится статус запроса, координаты дома и его полный адрес.
    :param address: адрес интересующего дома
    :return: объект YandexAPIData, содержащий статус поиска и найденную информацию
    """
    # Если в адресе не указан город, то добавляем его в конец адреса
    if 'Санкт-Петербург' not in str(address):
        address = append_city_name(address)

    apikey = '2d140aa9-59d0-44d8-bae8-2952b2154ed1'
    response = requests.get(
        f'https://geocode-maps.yandex.ru/1.x?geocode={address}&apikey={apikey}&format=json'
    ).json()
    return parse_respond(response)
