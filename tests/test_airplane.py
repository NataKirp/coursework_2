from src.airplane import Airplane


def test_cast_to_object_list_success(api_response):
    """Тестирование метода преобразования данных JSON в объекты класса."""
    result = Airplane.cast_to_object_list(api_response)

    assert len(result) == 2
    assert isinstance(result[0], Airplane)
    assert result[0].icao24 == "a123"
    assert result[0].callsign == "AFL123"
    assert result[0].country == "Russia"
    assert result[0].geo_altitude == 10500.5
    assert result[1].icao24 == "b456"


def test_cast_to_object_list_empty():
    """Тестирование работы метода при пустых данных."""
    api_response = {"states": None}
    result = Airplane.cast_to_object_list(api_response)
    assert result == []

    api_response_none = None
    result_none = Airplane.cast_to_object_list(api_response_none)
    assert result_none == []


def test_cast_to_object_list_bad_data():
    """Тестирование обработки некорректных данных от API."""
    api_bad_data = {
        "states": [
            [
                "a1",
                "CALL1",
                "Russia",
                0,
                0,
                0,
                0,
                10000.0,
                False,
                200,
                0,
                0,
                None,
                10000.0,
                "1",
                False,
                0,
            ],
            ["a2", "BAD"],
            None,
        ]
    }

    result = Airplane.cast_to_object_list(api_bad_data)

    assert len(result) == 1
    assert result[0].icao24 == "a1"
