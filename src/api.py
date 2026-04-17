from abc import ABC, abstractmethod

from requests import get, RequestException


class AeroplanesAPI(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def connect_to_api(self, country: str) -> None:
        """Метод для установки соединения с API"""
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> None:
        pass


class APIAdapter(AeroplanesAPI):

    def __init__(self) -> None:
        self.__aeroplanes = None
        self.__openstreetmap_url = 'https://nominatim.openstreetmap.org/search'
        self.__opensky_url = 'https://opensky-network.org/api/states/all?'

    def __get_geo_coordinates(self, country: str) -> dict:
        """Метод подключения к API для получения географических координат страны"""
        headers_nominatim = {
            'User-Agent': 'test-app/1.0',
        }
        # Указываем параметры: в каком формате возвращать данные и максимальную длину списка стран в ответе.
        params_nominatim = {
            'country': country,
            'format': 'json',
            'limit': 1,
        }
        try:
            response_nominatim = get(url=self.__openstreetmap_url, params=params_nominatim, headers=headers_nominatim)
            response_nominatim.raise_for_status()  # Вызовет ошибку, если статус не 200
            data = response_nominatim.json()
            return data[0].get('boundingbox')
        except RequestException as e:
            raise Exception(f'Не удалось получить гео координаты страны: {str(e)}')

    def __filter_aeroplanes(self, geo_coordinates: list) -> dict:
        """Метод подключения к API для получения данных о самолетах, находящихся в заданных координатах"""

        # Параметры для фильтрации самолетов по их географическим координатам.
        params_opensky = {
            'lamin': geo_coordinates[0],
            'lamax': geo_coordinates[1],
            'lomin': geo_coordinates[2],
            'lomax': geo_coordinates[3],
        }
        try:
            response_opensky = get(url=self.__opensky_url, params=params_opensky)
            response_opensky.raise_for_status()  # Вызовет ошибку, если статус не 200
            return response_opensky.json()
        except RequestException as e:
            raise Exception(f'Не удалось получить перечень самолетов: {str(e)}')

    def get_aeroplanes(self, country: str) -> None:
        """Метод получения данных о самолетах, находящихся в воздушном пространстве страны"""
        self.connect_to_api(country)

    def connect_to_api(self, country: str) -> None:
        """Метод подключения к API сервисов nominatim.openstreetmap.org и opensky-network.org"""

        country_coordinates = self.__get_geo_coordinates(country)
        self.__aeroplanes = self.__filter_aeroplanes(list(country_coordinates))


if __name__ == '__main__':
    api = APIAdapter()
    api.get_aeroplanes('Canada')
    # print(api.aeroplanes)
    print(api._APIAdapter__aeroplanes)
