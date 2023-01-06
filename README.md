# Pet-project "В_Питере_Жить"


# Цель проекта:

Создать модель, предсказывающую цену недвижимости в Санкт-Петербурге на основании данных с avito.ru и реализовать телеграм бота для пользователя, чтобы он мог пользоваться представленным сервисом.

# Содержание работы:

## 1. Сбор данных для обучения

Данные собирались с сайта [avito.ru.](https://www.avito.ru/)

Для извлечения данных был написан [парсер](https://github.com/NeKonnnn/PetProject-price-real-estate-in-St.-Petersburg/blob/main/parser/avito_parser.py), который собирал данные с сайта и сохранял их в файлы.

## 2. Анализ данных и построение модели 

- [EDA_zero.ipynb](http://localhost:8888/notebooks/PetProject-price-real-estate-in-St.-Petersburg/notebooks/0.%20EDA_zero.ipynb) - ноутбук с самым общим анализом данных без выводов. Данный ноутбук был создан на основе надстройки pandas_profiling.
- [EDA_first.ipynb](http://localhost:8888/notebooks/PetProject-price-real-estate-in-St.-Petersburg/notebooks/1.%20EDA_first.ipynb) - в этом нотбуке был проведен первичный анализ данных, на основе которого были сделаны следующие выводы:
1. 
2.
3.
...
- [feature_engineering_and_preprocessing.ipynb](http://localhost:8888/notebooks/PetProject-price-real-estate-in-St.-Petersburg/notebooks/2.%20feature_engineering_and_preprocessing.ipynb). В этом ноутбуке была проведена основная часть работы, а именно были сгенерированы необходимые для построения модли новые фичи, а также была проведена очистка данных. В итоге получается датасет с уже готовыми и чистыми данными для создания модели.
- [model.ipynb](). Модель была построена на Catboost. 

## 3. Внедрение (создание телеграмм бота).





