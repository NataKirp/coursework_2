import pytest

from src.airplane import Airplane
from src.api import AirplanesAPI
from src.file_handler import JSONSaver


@pytest.fixture
def sample_planes():
    """Создает список тестовых объектов Airplane."""
    return [
        Airplane(
            icao24="a1",
            callsign="AFR1",
            country="France",
            geo_altitude=10000,
            velocity=200,
        ),
        Airplane(
            icao24="a2",
            callsign="RUS2",
            country="Russia",
            geo_altitude=5000,
            velocity=300,
        ),
        Airplane(
            icao24="a3",
            callsign="USA3",
            country="United States",
            geo_altitude=12000,
            velocity=150,
        ),
    ]


@pytest.fixture
def temp_saver(tmp_path):
    """Создает временный JSON-файл для тестов, который удалится сам."""
    test_file = tmp_path / "test_airplanes.json"
    return JSONSaver(str(test_file))


@pytest.fixture
def api():
    return AirplanesAPI()


@pytest.fixture
def api_response():
    return {
        "states": [
            [
                "a123",
                "AFL123  ",
                "Russia",
                1703669143,
                1703669143,
                30.5,
                55.2,
                10500.5,
                False,
                250.8,
                0,
                0,
                None,
                10500.5,
                "1234",
                False,
                0,
            ],
            [
                "b456",
                "DLH456  ",
                "Germany",
                1703669143,
                1703669143,
                10.2,
                45.1,
                8000.0,
                False,
                210.0,
                0,
                0,
                None,
                8000.0,
                "5678",
                False,
                0,
            ],
        ]
    }


@pytest.fixture
def json_data():
    return [
        {
            "icao24": "a1",
            "callsign": "R1",
            "country": "Russia",
            "geo_altitude": 1000.0,
            "velocity": 100.0,
        },
        {
            "icao24": "a2",
            "callsign": "F1",
            "country": "France",
            "geo_altitude": 5000.0,
            "velocity": 200.0,
        },
    ]
