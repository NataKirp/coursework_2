from typing import Any


class Airplane:
    """Класс для работы с информацией о самолетах."""
    country: str  # страна регистрации ВС
    callsign: str  # позывной рейса
    geo_altitude: float  # геометрическая высота (м)
    velocity: float  # горизонтальная скорость(м / с)

    __slots__ = ('country', 'callsign', 'geo_altitude', 'velocity')

    def __init__(self, country, callsign, geo_altitude, velocity):
        self.country = self.__validate_str(country)
        self.callsign = self.__validate_str(callsign)
        self.geo_altitude = self.__validate_number(geo_altitude)
        self.velocity = self.__validate_number(velocity)

    @staticmethod
    def __validate_str(value: Any) -> str:
        """Возвращает N/A, если пришла не строка или пусто."""
        if isinstance(value, str) and value.strip():
            return value.strip()
        return 'N/A'

    @staticmethod
    def __validate_number(value: Any) -> float:
        """Возвращает 0.0, если значение является не числом или None."""
        if isinstance(value, (int, float)):
            return float(value)
        return 0.0

    @classmethod
    def from_dict(cls, data_list):
        """Создает объект из списка 'states'."""
        return cls(data_list[2], data_list[1].strip(), data_list[13], data_list[9])

    @classmethod
    def cast_to_object_list(cls, data) -> list:
        """Создает список объектов из набора данных."""
        if 'states' in data:
            return [cls.from_dict(item) for item in data['states']]
        else:
            raise ValueError('Данные не содержат ключ "states"')

    def __ge__(self, other):
        # для фильтрации по высоте
        val = other.geo_altitude if isinstance(other, Airplane) else other
        return self.geo_altitude >= val

    def __le__(self, other):
        # для фильтрации по высоте
        val = other.geo_altitude if isinstance(other, Airplane) else other
        return self.geo_altitude <= val

    def __lt__(self, other):
        # для сортировки по высоте
        val = other.geo_altitude if isinstance(other, Airplane) else other
        return self.geo_altitude < val

    def to_dict(self):
        """Возвращает объект в виде словаря, для проверки работы метода cast_to..."""
        # создает словарь с атрибутами объекта
        return {attr: getattr(self, attr) for attr in self.__slots__}
