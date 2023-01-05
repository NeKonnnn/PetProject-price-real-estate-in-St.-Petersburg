from typing import Dict

HELP_INFO = """
<b>/start</b> - <em>запускает бота</em>
<b>/estimate</b> - <em>Оценить стоимость квартиры по характеристикам</em>
<b>/repository</b> - <em>Предоставляет ссылку на гитхаб репозиторий с проектом</em>
<b>/help</b> - <em>Список команд</em>
<b>/about</b> - <em>Информация о боте</em>
"""

ABOUT_INFO = """
<b>НАШ БОТ</b>
<b>Что делает?</b> - <em>Данный бот предназначен для приблизительной оценки цены квартир в Санкт-Петербурге.</em>
<b>Как это устроено?</b> - <em>Мы собираем актуальную информацию с открытых торговых площадок, и на ее основе прикидываем стоимость.</em>
<b>Запутался?</b> - <em>Введи /help</em>
"""

START_ESTIMATION = """
На каждом шаге будет предложено ввести значение для параметра.\n
Чем больше параметров введете - тем точнее предсказанная цена.
Если что-то пошло не так, можете ввести или нажать на /restart и начнете заново.
"""

GITHUB_LINK = """
Вот наш гитхаб репозиторий:
https://github.com/NeKonnnn/PetProject-price-real-estate-in-St.-Petersburg
Но лучше туда не лезь))
"""

service_not_available_respond_text = 'К сожалению, сервис на данный момент не доступен, попробуйте позже.'

text_output_for_command = {
    'help': HELP_INFO,
    'about': ABOUT_INFO,
    'repository': GITHUB_LINK,
}

feature_names_for_message = {
    'address': 'Адрес квартиры',
    'rooms': 'Количество комнат',
    'total_area': 'Площадь квартиры',
    'stage': 'Этаж',
    'elevator': 'Есть ли лифт?',
    'largage_elevator': 'Есть ли грузовой лифт?',
}


def format_user_features(data: Dict) -> str:
    """Форматирует собранные фичи в удобочитаемую строку."""
    features_repr = '🏢 Вы ввели слудующие данные о квартире:🏢\n'
    for feature_name, cyr_name in feature_names_for_message.items():
        value = data[feature_name]
        if feature_name in {'largage_elevator', 'elevator'}:
            value = 'да' if value else 'нет'
        if feature_name == 'rooms':
            value = value if value else '0 (студия)'
        features_repr += f'{cyr_name} -> <b>{value}</b>\n'
    return features_repr


def format_model_response(model_response: Dict[str, float]) -> str:
    """Форматирует ответ API модели в удобочитаемую строку."""
    return f"""\n⭐️Результаты оценки⭐️
Квадратный метр ≈ 😱<b>{model_response['m2_price'] / 1_000:.1f} т.р./м2</b>😱
Общая стоимость ≈ 💲<b>{model_response['total_price'] / 1_000_000:.1f} млн. рублей</b>💲.

👍Спасибо за использование нашего бота!👍
Хочешь еще? - нажми ➡️ /estimate)
"""
