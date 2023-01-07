# Pet-project "В_Питере_Жить"

![preview](https://github.com/NeKonnnn/PetProject-price-real-estate-in-St.-Petersburg/blob/main/Peterss.jpg)

# Цель проекта:

Создать модель, предсказывающую цену недвижимости в Санкт-Петербурге на основании данных с avito.ru и реализовать телеграм бота для пользователя, чтобы он мог пользоваться представленным сервисом.

# Содержание работы:

## 1. Сбор данных для обучения

Данные собирались с сайта [avito.ru.](https://www.avito.ru/)

Для извлечения данных был написан [парсер](https://github.com/NeKonnnn/PetProject-price-real-estate-in-St.-Petersburg/blob/main/parser/avito_parser.py), который собирал данные с сайта и сохранял их в файлы.

## 2. Анализ данных и построение модели 

Сама [модель](https://github.com/NeKonnnn/PetProject-price-real-estate-in-St.-Petersburg/blob/main/notebooks/catboost/2211_pet_proj_property_2.ipynb)
 построена на Catboost. На тестовой выборке MAPE показало 16%, что является весьма неплохим результатом. 
 
## 3. Внедрение (создание телеграмм бота).

![qr_code](https://github.com/NeKonnnn/PetProject-price-real-estate-in-St.-Petersburg/blob/main/qr.png)





