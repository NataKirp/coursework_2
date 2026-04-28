from unittest.mock import MagicMock

from src.airplane import Airplane
from src.utils import (filter_airplanes, get_top_airplanes, handle_results,
                       sort_airplanes)


def test_filter_airplanes(json_data):
    """Тестирование фильтрации по заданному значению."""
    fake_saver = MagicMock()
    fake_saver.get_airplanes.return_value = json_data

    result = filter_airplanes(fake_saver, ["Russia"])

    assert len(result) == 2
    assert isinstance(result[0], Airplane)


def test_sort_airplanes():
    """Тестирование сортировки по высоте."""
    plane_low = Airplane(
        icao24="1", geo_altitude=1000, country="Russia", callsign="R1", velocity=100
    )
    plane_high = Airplane(
        icao24="2", geo_altitude=5000, country="Russia", callsign="R2", velocity=200
    )

    result = sort_airplanes([plane_low, plane_high])
    assert result[0].geo_altitude == 5000

    assert sort_airplanes([]) == []


def test_get_top_airplanes_less_n(capsys):
    """Тестирование работы функции, если самолетов меньше, чем в запросе пользователя."""
    planes = [
        Airplane(
            icao24="1", geo_altitude=1000, country="Russia", callsign="R1", velocity=100
        ),
        Airplane(
            icao24="2", geo_altitude=5000, country="Russia", callsign="R2", velocity=200
        ),
    ]

    result = get_top_airplanes(planes, 5)

    captured = capsys.readouterr()
    assert len(result) == 2
    assert "что меньше запрошенных" in captured.out


def test_get_top_airplanes_empty(capsys):
    """Тестирование работы функции при отсутствии данных для сортировки."""
    result = get_top_airplanes([], 5)

    captured = capsys.readouterr()
    assert result == []
    assert "Нет данных для отображения" in captured.out


def test_handle_results(monkeypatch, tmp_path):
    """Тестирование пользовательского интерфейса."""
    monkeypatch.setattr("src.file_handler.config.DATA_DIR", tmp_path)
    # Имитируем что пользователь выбрал '2' (сохранить) и нажал Enter (дефолтное имя)
    planes = [
        Airplane(
            icao24="test",
            geo_altitude=1000,
            country="Russia",
            callsign="R1",
            velocity=100,
        )
    ]
    user_input = iter(["2", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(user_input))
    # Вызываем с длинным списком стран
    countries = ["Russia", "France", "Germany", "United States"]
    handle_results(planes, "Test title", countries)

    # Проверяем, что имя файла содержит "and_others" и дату
    # Нам нужно найти созданный файл в tmp_path
    created_files = list(tmp_path.glob("*.json"))
    assert len(created_files) == 1
    filename = created_files[0].name
    assert "russia_france_and_others" in filename
