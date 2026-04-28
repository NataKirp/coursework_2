import pytest


def test_get_airplanes(api, requests_mock):
    """Тестирование успешного получения координат и самолетов."""
    country = "Russia"
    # имитация ответа от nominatim
    requests_mock.get(
        "https://nominatim.openstreetmap.org/search",
        json=[{"boundingbox": ["50", "60", "30", "40"]}],
    )
    # имитация ответа от opensky
    requests_mock.get(
        "https://opensky-network.org/api/states/all?",
        json={
            "states": [
                [
                    "icao1",
                    "call1",
                    "Russia",
                    1703669143,
                    1703669143,
                    30,
                    60,
                    10000,
                    False,
                    200,
                    0,
                    0,
                    None,
                    10000,
                    "1234",
                    False,
                    0,
                ]
            ]
        },
    )
    api.get_airplanes(country)

    assert api.airplanes is not None
    assert "states" in api.airplanes
    assert api.airplanes["states"][0][2] == "Russia"


def test_get_geo_coordinates_api_connection_error(api, requests_mock):
    """Тестирование обработки ошибок доступа к API."""
    requests_mock.get("https://nominatim.openstreetmap.org/search", status_code=500)

    with pytest.raises(Exception) as e:
        api.get_geo_coordinates("Russia")

    assert "Ошибка доступа к API" in str(e)


def test_get_geo_coordinates_no_country(api, requests_mock):
    """Тестирование работы функции при неизвестном названии страны."""
    requests_mock.get("https://nominatim.openstreetmap.org/search", json=[])

    result = api.get_geo_coordinates("Unknown")
    assert result is None
