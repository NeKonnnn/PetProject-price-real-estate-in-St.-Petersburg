from catboost import CatBoostRegressor
from fastapi import FastAPI
from pydantic.dataclasses import dataclass

# uvicorn main:model_application --reload
model_application = FastAPI()
# Последовательность фичей, использованная при тренировке модели
features_sequence = (
    'rooms',
    'total_area',
    'stage',
    'latitude',
    'longitude',
    'komendatskiy_prospekt_dist',
    'krestovskiy_ostrov_dist',
    'shushary_dist',
    'parnas_dist',
    'kupchino_dist',
    'ulitsa_dybenko_dist',
    'devyatkino_dist',
    'prospekt_veteranov_dist',
    'balcony',
    'building_age',
    'largage_elevator',
    'elevator',
)
loaded_model = CatBoostRegressor().load_model('catboost_model.cbm')


@dataclass
class ModelFeatures:
    rooms: int
    total_area: float
    stage: int
    latitude: float
    longitude: float
    komendatskiy_prospekt_dist: float
    krestovskiy_ostrov_dist: float
    shushary_dist: float
    parnas_dist: float
    kupchino_dist: float
    ulitsa_dybenko_dist: float
    devyatkino_dist: float
    prospekt_veteranov_dist: float
    balcony: bool
    building_age: int
    largage_elevator: bool
    elevator: bool


def format_features(features: ModelFeatures):
    """Форматирует словарь фичей в необходимый для модели формат."""
    return [features.__dict__[feature_name] for feature_name in features_sequence]


@model_application.post('/get_model_prediction')
async def get_prediction(features: ModelFeatures) -> dict:
    prediction = loaded_model.predict(data=format_features(features))
    return {'m2_price': prediction, 'total_price': prediction * features.total_area}
