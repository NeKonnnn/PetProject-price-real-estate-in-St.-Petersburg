from aiogram.dispatcher.filters.state import StatesGroup, State


class ClientStates(StatesGroup):
    """Последовательность опроса пользователя по параметрам квартиры."""
    main_menu = State()
    address = State()
    number_of_rooms = State()
    total_area = State()
    stage = State()
    balcony = State()
    elevator = State()
    largage_elevator = State()
    model_response = State()
