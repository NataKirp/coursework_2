from typing import Any


class Airplane:
    """Класс для работы с информацией о самолетах."""
    icao24: str  # уникальный идентификатор борта
    callsign: str  # позывной рейса
    country: str  # страна регистрации ВС
    geo_altitude: float  # геометрическая высота (м)
    velocity: float  # горизонтальная скорость(м / с)

    __slots__ = ('icao24', 'callsign', 'country', 'geo_altitude', 'velocity')

    def __init__(self, icao24, callsign, country, geo_altitude, velocity):
        self.icao24 = self.__validate_str(icao24)
        self.callsign = self.__validate_str(callsign)
        self.country = self.__validate_str(country)
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
        return cls(data_list[0], data_list[1].strip(), data_list[2], data_list[13], data_list[9])

    @classmethod
    def cast_to_object_list(cls, data) -> list:
        """Создает список объектов из набора данных."""
        if 'states' in data:
            return [cls.from_dict(item) for item in data['states']]
        else:
            raise ValueError('Данные не содержат ключ "states"')

    def __ge__(self, other):
        # для фильтрации по высоте
        if isinstance(other, Airplane):
            return self.geo_altitude >= other.geo_altitude
        if isinstance(other, (int, float)):
            return self.geo_altitude >= other
        return NotImplemented

    def __le__(self, other):
        # для фильтрации по высоте
        if isinstance(other, Airplane):
            return self.geo_altitude <= other.geo_altitude
        if isinstance(other, (int, float)):
            return self.geo_altitude <= other
        return NotImplemented

    def __lt__(self, other):
        # для сортировки по высоте
        if isinstance(other, Airplane):
            return self.geo_altitude < other.geo_altitude
        if isinstance(other, (int, float)):
            return self.geo_altitude < other

    def to_dict(self) -> dict:
        """Возвращает объект в виде словаря, для сохранения в JSON."""
        # создает словарь с атрибутами объекта
        return {attr: getattr(self, attr) for attr in self.__slots__}
