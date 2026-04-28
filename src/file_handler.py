import os.path
from abc import ABC, abstractmethod
import json
from json import JSONDecodeError

import config
from src.airplane import Airplane


class FileHandler(ABC):
    """Абстрактный класс для работы с файлами."""

    @abstractmethod
    def add_airplane(self, plane) -> None:
        """Добавляет данные о самолете в файл."""
        pass

    @abstractmethod
    def get_airplanes(self, criteria: dict) -> list:
        """Получает данные о самолетах из файла по указанным критериям"""
        pass

    @abstractmethod
    def delete_airplane(self, icao24: str) -> None:
        """Удаляет данные о самолете из файла по ID борта."""
        pass


class JSONSaver(FileHandler):
    """Класс для работы с данными в формате Json."""

    def __init__(self, filename=None):
        """Инициализация приватного атрибута - имени файла."""
        if filename is None:
            self.__filename = config.PLANES_JSON_PATH
        else:
            self.__filename = config.DATA_DIR / filename

        if not os.path.exists(self.__filename):
            self._save_file([])

    def _read_file(self) -> list:
        """Внутренний метод для чтения данных."""
        try:
            with open(self.__filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (JSONDecodeError, FileNotFoundError):
            return []

    def _save_file(self, data: list):
        """Внутренний метод для записи данных."""
        with open(self.__filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def add_airplane(self, plane: Airplane) -> None:
        """Добавляет самолет в файл, если его там еще нет, или обновляет данные."""
        data = self._read_file()
        # ищем индекс самолета с таким же icao24 и меняем данные, если есть (на случай, когда изменилась высота и т.п.)
        for index, item in enumerate(data):
            if item.get('icao24') == plane.icao24:
                data[index] = plane.to_dict()
                self._save_file(data)
                return
        # если не найден самолет, добавляем новый
        data.append(plane.to_dict())
        self._save_file(data)

    def get_airplanes(self, criteria: dict) -> list:
        """Ищет данные в файле по критериям."""
        data = self._read_file()
        result = []

        for item in data:
            match = True
            for key, value in criteria.items():
                item_value = item.get(key)

                if isinstance(value, list):  # проверка, если передан список стран
                    if item_value not in value:
                        match = False
                        break
                elif isinstance(value, tuple) and len(
                        value) == 2:  # проверка, если передан диапазон (кортеж из 2 чисел)
                    if not (value[0] <= item_value <= value[1]):
                        match = False
                        break
                else:
                    if item_value != value:  # проверка, если передана строка или число (строгое совпадение)
                        match = False
                        break
            if match:
                result.append(item)
        return result

    def delete_airplane(self, icao24: str) -> bool:
        """Удаляет самолет по его icao24."""
        data = self._read_file()
        initial_length = len(data)
        new_data = [item for item in data if item.get('icao24') != icao24]

        self._save_file(new_data)

        return len(new_data) < initial_length

    def clear_airplanes(self):
        self._save_file([])
