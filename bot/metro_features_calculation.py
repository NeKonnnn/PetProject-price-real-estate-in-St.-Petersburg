from typing import Dict

import numpy as np

metro_coordinates = {
    'девяткино': {'Широта': 60.050182, 'Долгота': 30.443045},
    'проспект ветеранов': {'Широта': 59.84211, 'Долгота': 30.250588},
    'купчино': {'Широта': 59.829781, 'Долгота': 30.375702},
    'комендантский проспект': {'Широта': 60.008591, 'Долгота': 30.258663},
    'крестовский остров': {'Широта': 59.971821, 'Долгота': 30.259436},
    'шушары': {'Широта': 59.819973, 'Долгота': 30.432718},
    'парнас': {'Широта': 60.06699, 'Долгота': 30.333839},
    'улица дыбенко': {'Широта': 59.907417, 'Долгота': 30.483311},
}

metro_names_to_latin_mapper = {
    'комендантский проспект': 'komendatskiy_prospekt',
    'крестовский остров': 'krestovskiy_ostrov',
    'шушары': 'shushary',
    'парнас': 'parnas',
    'купчино': 'kupchino',
    'улица дыбенко': 'ulitsa_dybenko',
    'девяткино': 'devyatkino',
    'проспект ветеранов': 'prospekt_veteranov',
}


def get_distance_to_metro(house_latitude: float, house_longitude: float, metro_name: str) -> float:
    """Рассчитывает расстояние в километрах от дома до станции метро."""
    latitude_part = (house_latitude - metro_coordinates[metro_name]['Широта']) ** 2
    longitude_part = (house_longitude - metro_coordinates[metro_name]['Долгота']) ** 2
    # преобразование во float нужно для дальнейшей возможности отправки словаря в json'е request'а
    return float(
        round(np.sqrt(latitude_part + longitude_part) * 111.13, 3)
    )


def calculate_metro_distances(house_latitude: float, house_longitude: float) -> Dict[str, float]:
    """Рассчитывает расстояние до выбранных метро."""
    distances = {}
    for metro_name, latin_name in metro_names_to_latin_mapper.items():
        distances[f'{latin_name}_dist'] = get_distance_to_metro(house_latitude, house_longitude, metro_name)
    return distances
