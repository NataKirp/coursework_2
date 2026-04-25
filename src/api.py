from abc import ABC, abstractmethod
from typing import Optional

import requests
from requests import RequestException


class APIAdapter(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def _connect_to_api(self, url: str, params: dict[str, any], headers: Optional[dict[str, str]]) -> requests.Response:
        """Абстрактный метод для установки соединения с API"""
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> None:
        """Абстрактный метод для получения информации о самолетах"""
        pass


class AeroplanesAPI(APIAdapter):
    """Класс для получения данных о полетах с сервисов nominatim.openstreetmap.org и opensky-network.org."""

    def __init__(self) -> None:
        """Инициализация приватных атрибутов класса и хранилища."""
        self.__openstreetmap_url = 'https://nominatim.openstreetmap.org/search'
        self.__opensky_url = 'https://opensky-network.org/api/states/all?'
        self.aeroplanes = None

    def _connect_to_api(self, url: str, params: dict[str, any], headers: Optional[dict[str, str]]) -> requests.Response:
        """Метод подключения к API с проверкой статус-кода ответа."""
        try:
            response = requests.get(url=url, params=params, headers=headers)
            response.raise_for_status()  # Вызовет ошибку, если статус не 200
            return response
        except RequestException as e:
            raise Exception(f'Ошибка доступа к API: {str(e)}')

    def get_geo_coordinates(self, country: str) -> dict:
        """Метод подключения к API для получения географических координат страны"""
        headers_nominatim = {
            'User-Agent': 'test-app/1.0',
        }
        # указываем параметры: в каком формате возвращать данные и максимальную длину списка стран в ответе.
        params_nominatim = {
            'country': country,
            'format': 'json',
            'limit': 1,
        }
        response_nominatim = self._connect_to_api(self.__openstreetmap_url, params_nominatim, headers_nominatim)
        data = response_nominatim.json()

        if not data:
            print(f'Страна {country} не найдена')

        return data[0].get('boundingbox')

    def filter_aeroplanes(self, geo_coordinates: list) -> dict:
        """Метод подключения к API для получения данных о самолетах, находящихся в заданных координатах"""
        # параметры для фильтрации самолетов по их географическим координатам.
        params_opensky = {
            'lamin': geo_coordinates[0],
            'lamax': geo_coordinates[1],
            'lomin': geo_coordinates[2],
            'lomax': geo_coordinates[3],
        }
        response_opensky = self._connect_to_api(self.__opensky_url, params_opensky, None)
        return response_opensky.json()

    def get_aeroplanes(self, country: str) -> None:
        """Метод получения данных о самолетах, находящихся в воздушном пространстве страны"""
        country_coordinates = self.get_geo_coordinates(country)
        self.aeroplanes = self.filter_aeroplanes(list(country_coordinates))

# if __name__ == '__main__':
#     api = AeroplanesAPI()
#     api.get_aeroplanes('Canada')
#     print(api.aeroplanes)
